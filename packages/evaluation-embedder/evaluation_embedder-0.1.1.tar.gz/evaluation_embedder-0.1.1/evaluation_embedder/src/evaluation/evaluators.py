from typing import List, cast

import numpy as np
from langchain_core.documents import Document

from evaluation_embedder.src.datasets.polars import PolarsTextDataset
from evaluation_embedder.src.evaluation import Evaluator
from evaluation_embedder.src.evaluation.vector_stores import FaissVectorStore
from evaluation_embedder.src.settings import (
    FaissEvaluatorSettings,
    QdrantEvaluatorSettings,
)


class QdrantEvaluator(Evaluator[QdrantEvaluatorSettings]):
    def __init__(self, config: QdrantEvaluatorSettings):
        super().__init__(config)


class FaissEvaluator(Evaluator[FaissEvaluatorSettings]):
    def __init__(self, config: FaissEvaluatorSettings):
        super().__init__(config)

    @classmethod
    async def create(cls, config: FaissEvaluatorSettings) -> "FaissEvaluator":
        self = cls(config)

        docs = self.get_docs()
        texts = [d.page_content for d in docs]

        embeddings = np.asarray(
            await self.retriever.embedder.aembed_documents(texts),
            dtype="float32",
        )

        vector_store = cast(FaissVectorStore, self.retriever.vector_store)
        vector_store.index = vector_store.build_faiss_index(embeddings.shape[-1])
        vector_store.add_documents(docs, embeddings)

        return self

    def get_docs(self) -> List[Document]:
        docs_idx = []
        seen = set()
        for i, row in enumerate(self.dataset.iter_rows(named=True)):
            doc_id = row["metadata"]["doc_id"]
            if doc_id not in seen:
                seen.add(doc_id)
                docs_idx.append(i)
        return PolarsTextDataset(self.dataset.polars[docs_idx]).to_langchain_documents()
