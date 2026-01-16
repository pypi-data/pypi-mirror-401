from typing import Union, cast

import polars as pl

from evaluation_embedder.src.constants import TDataset
from evaluation_embedder.src.datasets import TextDataset


class PolarsTextDataset(TextDataset[Union[pl.DataFrame, pl.LazyFrame]]):

    def __init__(self, service: Union[pl.DataFrame, pl.LazyFrame]):
        super().__init__(service)

    @classmethod
    def from_polars(cls, df: Union[pl.DataFrame, pl.LazyFrame]) -> "TextDataset[TDataset]":
        return cast("TextDataset[TDataset]", cls(df))

    def to_polars(self) -> pl.DataFrame:
        if isinstance(self.service, pl.LazyFrame):
            return self.service.collect()
        return self.service

    def to_lazy_polars(self) -> pl.LazyFrame:
        if isinstance(self.service, pl.LazyFrame):
            return self.service
        return self.service.lazy()
