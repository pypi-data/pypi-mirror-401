import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Generic, Iterator, List, Optional, Tuple, cast

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
from langchain_core.documents import (
    Document,  # or: from langchain.schema import Document
)
from pydantic import BaseModel, Field

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
    MAX_BATCH_SIZE = 64
    BATCH_TIMEOUT_MS = 45

    def __init__(self, config: TCEmbedder) -> None:
        self.config = config
        self._queue: asyncio.Queue[Tuple[str, asyncio.Future[List[float]]]] = asyncio.Queue()
        self._batch_task: asyncio.Task | None = None
        _logger.info(f"Initialized Embedder | class={self.__class__.__name__}")

    # ---------------- ABSTRACT ----------------

    @abstractmethod
    async def _aembed(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError()

    # ---------------- BATCH WORKER ----------------

    async def _batch_worker(self) -> None:
        while True:
            batch: list[Tuple[str, asyncio.Future[List[float]]]] = []

            start = time.monotonic()

            while len(batch) < self.MAX_BATCH_SIZE:
                timeout = self.BATCH_TIMEOUT_MS / 1000 - (time.monotonic() - start)
                if timeout <= 0:
                    break

                try:
                    item = await asyncio.wait_for(self._queue.get(), timeout)
                    batch.append(item)
                except asyncio.TimeoutError:
                    break

            if not batch:
                continue
            futures = [fut for _, fut in batch]
            try:
                embeddings = await self._aembed([text for text, _ in batch])
                for fut, emb in zip(futures, embeddings):
                    fut.set_result(emb)
            except Exception as e:
                for fut in futures:
                    fut.set_exception(e)

    def _ensure_batch_task(self) -> None:
        if self._batch_task is None or self._batch_task.done():
            self._batch_task = asyncio.create_task(self._batch_worker())

    # ---------------- PUBLIC API ----------------

    async def aembed(self, texts: List[str]) -> List[List[float]]:

        self._ensure_batch_task()

        futures: list[asyncio.Future[List[float]]] = []

        for text in texts:
            fut: asyncio.Future[List[float]] = asyncio.get_running_loop().create_future()
            await self._queue.put((text, fut))
            futures.append(fut)

        return await asyncio.gather(*futures)

    async def aembed_query(
        self,
        text: str,
        processor: Optional[Processor[Any]] = None,
    ) -> List[float]:
        if processor:
            text = processor(text=text, purpose=EmbeddingPurposeEnum.QUERY)  # type: ignore[arg-type]
        return (await self.aembed([text]))[0]

    async def aembed_documents(
        self,
        texts: List[str],
        processor: Optional[Processor[Any]] = None,
    ) -> List[List[float]]:
        if processor:
            texts = [processor(text=text, purpose=EmbeddingPurposeEnum.DOCUMENT) for text in texts]  # type: ignore[arg-type]
        return await self.aembed(texts)


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
    BATCH_SIZE = 96

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

    def batch_iter(self) -> Iterator[list[dict[str, Any]]]:
        batch: list[dict[str, Any]] = []
        for row in self.dataset.iter_rows(named=True):
            batch.append(row)
            if len(batch) == self.BATCH_SIZE:
                yield batch
                batch = []
        if batch:
            yield batch

    async def eval(self) -> List[List[Score.ScoreResult]]:
        scores_all: list[list[Score.ScoreResult]] = []

        max_k = max(getattr(score.config, "k", 0) for score in self.scores)
        _logger.info(f"Starting evaluation | max_k={max_k} | num_queries={len(self.dataset)}")

        processed = 0

        for batch in self.batch_iter():
            # Prepare async retrieval tasks
            tasks: list[asyncio.Task] = []

            for sample in batch:
                query = sample["metadata"]["query"]

                tasks.append(
                    asyncio.create_task(
                        self.retriever.retrieve(
                            query=query,
                            limit=max_k,
                        )
                    )
                )

            # Run retrieval concurrently
            responses = await asyncio.gather(*tasks)

            # Compute scores
            for sample, response in zip(batch, responses):
                page_content = self.retriever.processor(
                    sample["page_content"],
                    purpose=EmbeddingPurposeEnum.DOCUMENT,  # type: ignore[arg-type]
                )

                hits = [p.document.page_content == page_content for p in response.points]

                scores = [score(hits) for score in self.scores]
                scores_all.append(scores)

                processed += 1
                if processed % self.__class__.NB_LOGS_PER_QUERIES == 0 or processed == len(self.dataset):
                    _logger.info(f"Eval progress | processed={processed}/{len(self.dataset)}")

        _logger.info("Evaluation completed")
        return scores_all
