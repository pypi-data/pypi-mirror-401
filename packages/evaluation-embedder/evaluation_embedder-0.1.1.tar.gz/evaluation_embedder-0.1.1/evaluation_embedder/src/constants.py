from typing import TYPE_CHECKING, Literal, TypeAlias, TypeVar

from polars import Enum

if TYPE_CHECKING:
    from evaluation_embedder.src.settings import (
        DatasetSettings,
        EmbedderSettings,
        EvaluatorSettings,
        FromConfigMixinSettings,
        ProcessorSettings,
        RetrieverSettings,
        ScoreSettings,
        VectorStoreSettings,
    )

CONFIG_PATH = "/config/config.yaml"

TDataset = TypeVar("TDataset")
ParquetCompression: TypeAlias = Literal["lz4", "uncompressed", "snappy", "gzip", "brotli", "zstd"]
TCFromConfigMixin = TypeVar("TCFromConfigMixin", bound="FromConfigMixinSettings")
TCDataset = TypeVar("TCDataset", bound="DatasetSettings")
TCEmbedder = TypeVar("TCEmbedder", bound="EmbedderSettings")
TCEvaluator = TypeVar("TCEvaluator", bound="EvaluatorSettings")
TCProcessor = TypeVar("TCProcessor", bound="ProcessorSettings")
TCRetriever = TypeVar("TCRetriever", bound="RetrieverSettings")
TCScore = TypeVar("TCScore", bound="ScoreSettings")
TCVectorStore = TypeVar("TCVectorStore", bound="VectorStoreSettings")


class EmbeddingPurposeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"


class FAISSIndexType(Enum):
    FLAT_IP = "flat_ip"
    FLAT_L2 = "flat_l2"
