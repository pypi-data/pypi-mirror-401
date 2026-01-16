import io
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Self,
    Tuple,
    Union,
    cast,
    overload,
)

import polars as pl
from langchain_core.documents import Document
from minio import Minio
from polars._typing import ColumnNameOrSelector, IntoExpr, IntoExprColumn

from evaluation_embedder.src.constants import ParquetCompression, TDataset
from evaluation_embedder.src.settings import (
    MinioDatasetSettings,
    ParquetDatasetSettings,
)

_logger = logging.getLogger(__name__)


class Dataset(ABC, Generic[TDataset]):
    def __init__(self, service: TDataset):
        super().__init__()
        self.service = service
        self._polars: Optional[pl.DataFrame] = None
        self._lazy_polars: Optional[pl.LazyFrame] = None

    @classmethod
    @abstractmethod
    def from_polars(cls, df: Union[pl.DataFrame, pl.LazyFrame]) -> "Dataset[TDataset]":
        raise NotImplementedError

    @abstractmethod
    def to_polars(self) -> pl.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def to_lazy_polars(self) -> pl.LazyFrame:
        raise NotImplementedError

    @classmethod
    def from_parquet(
        cls,
        path: Union[str, Path],
        *,
        lazy: bool = True,
    ) -> "Dataset[TDataset]":
        df: Union[pl.DataFrame, pl.LazyFrame]
        if lazy:
            df = pl.scan_parquet(path)
        else:
            df = pl.read_parquet(path)

        return cls.from_polars(df)

    @classmethod
    def from_minio(
        cls,
        *,
        bucket: str,
        key: str,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
    ) -> "Dataset[TDataset]":
        client = Minio(
            endpoint_url.replace("http://", "").replace("https://", ""),
            access_key=access_key,
            secret_key=secret_key,
            secure=endpoint_url.startswith("https://"),
        )
        response = client.get_object(bucket, key)
        try:
            buffer = io.BytesIO(response.read())
        finally:
            response.close()
            response.release_conn()

        df = pl.read_parquet(buffer)
        return cls.from_polars(df)

    @property
    def polars(self) -> pl.DataFrame:
        if self._polars is None:
            self._polars = self.to_polars()
        return self._polars

    @property
    def lazy_polars(self) -> pl.LazyFrame:
        if self._lazy_polars is None:
            self._lazy_polars = self.to_lazy_polars()
        return self._lazy_polars

    @property
    def polars_shape(self) -> Tuple[int, int]:
        return self.polars.shape

    @classmethod
    def from_documents(cls, docs: List[Document]) -> "TextDataset[TDataset]":
        df = pl.DataFrame(
            {
                "page_content": [d.page_content for d in docs],
                "metadata": [d.metadata or {} for d in docs],
            }
        )
        return cast(TextDataset[TDataset], cls.from_polars(df))

    def with_columns(
        self,
        *exprs: IntoExpr | Iterable[IntoExpr],
        **named_exprs: IntoExpr,
    ) -> "Dataset[TDataset]":
        df = self.polars.with_columns(*exprs, **named_exprs)
        return self.__class__.from_polars(df)

    def filter(
        self,
        *predicates: (IntoExprColumn | Iterable[IntoExprColumn] | bool | list[bool]),
        **constraints: Any,
    ) -> "Dataset[TDataset]":
        return self.__class__.from_polars(self.polars.filter(*predicates, **constraints))

    def drop(
        self,
        *columns: ColumnNameOrSelector | Iterable[ColumnNameOrSelector],
        strict: bool = True,
    ) -> "Dataset[TDataset]":
        return self.__class__.from_polars(self.polars.drop(*columns, strict=strict))

    def __len__(self) -> int:
        return self.polars_shape[0]

    @overload
    def iter_rows(self, *, named: Literal[False] = ..., buffer_size: int = ...) -> Iterator[Tuple[Any, ...]]: ...

    @overload
    def iter_rows(self, *, named: Literal[True], buffer_size: int = ...) -> Iterator[Dict[str, Any]]: ...

    def iter_rows(
        self, *, named: Literal[False, True] = False, buffer_size: int = 512
    ) -> Iterator[Tuple[Any, ...]] | Iterator[Dict[str, Any]]:
        df_stream = self.lazy_polars.collect(streaming=True)  # type: ignore[call-overload]
        return df_stream.iter_rows(named=named, buffer_size=buffer_size)  # type: ignore[no-any-return]


class TextDataset(Dataset[TDataset], Generic[TDataset]):
    REQUIRED_COLUMNS = {"page_content", "metadata"}

    def __init__(self, service: TDataset):
        super().__init__(service)
        self._validate_schema()

    def _validate_schema(self) -> None:
        df = self.polars
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(
                f"{self.__class__.__name__} requires columns {self.REQUIRED_COLUMNS}, " f"but missing {missing}"
            )

    def iter_documents(self) -> Iterator[Document]:
        for row in self.polars.iter_rows(named=True):
            yield Document(
                page_content=row["page_content"],
                metadata=row["metadata"],
            )

    def dump_documents(
        self,
        out_dir: str,
        prefix: str = "doc",
        ext: str = ".md",
        encoding: str = "utf-8",
    ) -> None:
        out_dir_path = Path(out_dir)
        out_dir_path.mkdir(parents=True, exist_ok=True)
        for i, row in enumerate(self.polars.iter_rows(named=True)):
            path = out_dir_path / f"{prefix}_{i:05d}{ext}"
            path.write_text(row["page_content"], encoding=encoding)

    def to_langchain_documents(
        self,
    ) -> list[Document]:
        docs: list[Document] = []
        for row in self.polars.iter_rows(named=True):
            docs.append(
                Document(
                    page_content=row["page_content"],
                    metadata=row["metadata"],
                )
            )
        return docs

    def to_minio(
        self,
        *,
        bucket: str,
        key: str,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        compression: ParquetCompression = "zstd",
        row_group_size: int = 100_000,
    ) -> None:
        client = Minio(
            endpoint_url.replace("http://", "").replace("https://", ""),
            access_key=access_key,
            secret_key=secret_key,
            secure=endpoint_url.startswith("https://"),
        )
        buffer = io.BytesIO()
        self.polars.write_parquet(
            buffer,
            compression=compression,
            row_group_size=row_group_size,
        )
        buffer.seek(0)
        client.put_object(
            bucket_name=bucket,
            object_name=key,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type="application/octet-stream",
        )

    @overload
    @classmethod
    def from_config(
        cls,
        config: ParquetDatasetSettings,
    ) -> Self: ...

    @overload
    @classmethod
    def from_config(
        cls,
        config: MinioDatasetSettings,
    ) -> Self: ...

    @classmethod
    def from_config(
        cls,
        config: Union[ParquetDatasetSettings, MinioDatasetSettings],
    ) -> Self:
        if isinstance(config, ParquetDatasetSettings):
            df = pl.scan_parquet(config.path) if config.lazy else pl.read_parquet(config.path)
            return cast(Self, cls.from_polars(df))
        if isinstance(config, MinioDatasetSettings):
            return cast(
                Self,
                cls.from_minio(
                    bucket=config.bucket,
                    key=config.key,
                    endpoint_url=config.endpoint,
                    access_key=config.access_key,
                    secret_key=config.secret_key,
                ),
            )

        raise TypeError(f"Unsupported dataset config: {type(config).__name__}")

    @classmethod
    def from_records(
        cls,
        records: List[Tuple[str, Dict[str, Any]]],
    ) -> "TextDataset[TDataset]":
        if not records:
            raise ValueError("records must be non-empty")
        df = pl.DataFrame(
            {
                "page_content": [text for text, _ in records],
                "metadata": [meta for _, meta in records],
            }
        )
        return cast("TextDataset[TDataset]", cls.from_polars(df))
