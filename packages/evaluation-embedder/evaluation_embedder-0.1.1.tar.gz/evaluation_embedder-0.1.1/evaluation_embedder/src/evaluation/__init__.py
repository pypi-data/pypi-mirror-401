import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, cast

from langchain_core.documents import (
    Document,  # or: from langchain.schema import Document
)
from pydantic import BaseModel, Field

from evaluation_embedder.src.constants import (
    EmbeddingPurposeEnum,
    TCEmbedder,
    TCEvaluator,
    TCProcessor,
    TCRetriever,
    TCScore,
    TCVectorStore,
)
from evaluation_embedder.src.datasets import TextDataset
from evaluation_embedder.src.mixins import FromConfigMixin
from evaluation_embedder.src.utils import load_class

_logger = logging.getLogger(__name__)


class Score(ABC, Generic[TCScore]):

    class ScoreResult(BaseModel):
        name: str
        value: float

    def __init__(self, config: TCScore) -> None:
        self.config = config
        _logger.info(f"Initialized Score | class={self.__class__.__name__} | config={config}")

    @abstractmethod
    def __call__(self, hits: List[bool]) -> ScoreResult:
        raise NotImplementedError()


class Processor(FromConfigMixin[TCProcessor], ABC, Generic[TCProcessor]):

    def __init__(self, config: TCProcessor) -> None:
        self.config = config

    @abstractmethod
    def __call__(self, text: str, purpose: EmbeddingPurposeEnum) -> str:
        raise NotImplementedError()


class Embedder(FromConfigMixin[TCEmbedder], ABC, Generic[TCEmbedder]):

    def __init__(self, config: TCEmbedder) -> None:
        self.config = config
        _logger.info(f"Initialized Embedder | class={self.__class__.__name__} | config={config}")

    @abstractmethod
    async def _aembed_documents(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError()

    def process_query(self, text: str, processor: Optional[Processor[Any]]) -> str:
        if processor:
            return processor(text=text, purpose=EmbeddingPurposeEnum.QUERY)  # type: ignore[arg-type]
        return text

    def process_document(self, text: str, processor: Optional[Processor[Any]]) -> str:
        if processor:
            return processor(text=text, purpose=EmbeddingPurposeEnum.DOCUMENT)  # type: ignore[arg-type]
        return text

    async def aembed_documents(
        self,
        texts: List[str],
        processor: Optional[Processor] = None,
    ) -> List[List[float]]:
        docs = [self.process_document(t, processor) for t in texts]
        return await self._aembed_documents(docs)

    async def aembed_query(self, text: str, processor: Optional[Processor] = None) -> List[float]:
        text = self.process_query(text, processor)
        return (await self.aembed_documents([text]))[0]


class VectorStore(FromConfigMixin[TCVectorStore], ABC, Generic[TCVectorStore]):
    class ScoredPoint(BaseModel):
        score: float = Field(..., description="Points vector distance to the query vector")
        document: Document

    class QueryResponse(BaseModel):
        points: List["VectorStore.ScoredPoint"]

    def __init__(self, config: TCVectorStore) -> None:
        self.config = config
        _logger.info(f"Initialized VectorStore | class={self.__class__.__name__} | config={config}")

    @abstractmethod
    def query_points(self, query: List[float], *, limit: int) -> QueryResponse:
        raise NotImplementedError()


class Retriever(FromConfigMixin[TCRetriever], ABC, Generic[TCRetriever]):

    def __init__(self, config: TCRetriever) -> None:
        self.config = config

        _logger.info(f"Initializing Retriever | class={self.__class__.__name__}")

        self.embedder: Embedder[Any] = load_class(self.config.embedder.module_path)(self.config.embedder)

        self.vector_store: VectorStore[Any] = load_class(self.config.vector_store.module_path)(self.config.vector_store)

        self.processor: Processor[Any] = load_class(self.config.processor.module_path)(self.config.processor)

        _logger.info(
            f"Retriever initialized | embedder={type(self.embedder).__name__} | "
            f"vector_store={type(self.vector_store).__name__}"
        )

    async def retrieve(self, query: str, *, limit: int) -> VectorStore.QueryResponse:
        query_embedding = await self.embedder.aembed_query(query, self.processor)
        return self.vector_store.query_points(
            query=query_embedding,
            limit=limit,
        )


class Evaluator(FromConfigMixin[TCEvaluator], ABC, Generic[TCEvaluator]):

    NB_LOGS_PER_QUERIES = 100

    def __init__(self, config: TCEvaluator) -> None:
        self.config = config

        _logger.info(f"Initializing Evaluator | class={self.__class__.__name__}")

        self.dataset: TextDataset[Any] = self._load_dataset()
        self.retriever: Retriever[Any] = load_class(self.config.retriever.module_path)(self.config.retriever)
        self.scores: List[Score[Any]] = [load_class(s.module_path)(s) for s in self.config.scores]

        _logger.info(
            f"Evaluator ready | dataset_size={len(self.dataset)} | " f"scores={[type(s).__name__ for s in self.scores]}"
        )

    def _load_dataset(self) -> TextDataset[Any]:
        dataset_cls = load_class(self.config.dataset.module_path)
        _logger.info(
            f"Instantiating dataset | class={dataset_cls.__name__} | " f"module_path={self.config.dataset.module_path}"
        )
        dataset = cast(
            TextDataset[Any],
            dataset_cls.from_config(self.config.dataset),
        )
        _logger.info(f"Dataset loaded | type={type(dataset).__name__} | " f"size={len(dataset)}")
        return dataset

    async def eval(self) -> List[List[Score.ScoreResult]]:
        scores_all = []
        max_k = max(getattr(score.config, "k", 0) for score in self.scores)
        _logger.info(f"Starting evaluation | max_k={max_k} | num_queries={len(self.dataset)}")
        for idx, sample in enumerate(self.dataset.iter_rows(named=True), start=1):
            scores = []
            query = sample["metadata"]["query"]
            page_content = self.retriever.processor(sample["page_content"], purpose=EmbeddingPurposeEnum.DOCUMENT)  # type: ignore[arg-type]
            response = await self.retriever.retrieve(
                query,
                limit=max_k,
            )
            hits = [p.document.page_content == page_content for p in response.points]
            scores = [s(hits) for s in self.scores]
            scores_all.append(scores)
            if idx % self.__class__.NB_LOGS_PER_QUERIES == 0 or idx == len(self.dataset):
                _logger.info(f"Eval progress | processed={idx}/{len(self.dataset)}")
        _logger.info("Evaluation completed")
        return scores_all
