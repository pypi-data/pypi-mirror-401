from typing import List, Optional

import faiss  # type:ignore[import-untyped]
import numpy as np
from langchain_core.documents import Document
from qdrant_client import QdrantClient

from evaluation_embedder.src.constants import FAISSIndexType
from evaluation_embedder.src.evaluation import VectorStore
from evaluation_embedder.src.evaluation.vector_stores import VectorStore
from evaluation_embedder.src.settings import (
    FaissVectorStoreSettings,
    QdrantVectorStoreSettings,
)


class FaissVectorStore(VectorStore[FaissVectorStoreSettings]):

    def __init__(self, config: FaissVectorStoreSettings):
        super().__init__(config)
        self.documents: List[Document] = []
        self.index: Optional[faiss.Index] = None

    def build_faiss_index(self, dim: int) -> faiss.Index:
        if self.config.index_type is FAISSIndexType.FLAT_IP:
            return faiss.IndexFlatIP(dim)
        return faiss.IndexFlatL2(dim)

    # --------------------------------------------------
    # Add documents
    # --------------------------------------------------
    def add_documents(
        self,
        documents: List[Document],
        embeddings: np.ndarray,
    ) -> None:
        if self.config.normalize:
            faiss.normalize_L2(embeddings)
        if self.index is None:
            raise ValueError(f"index should be created before adding documents")
        self.index.add(embeddings.astype("float32"))
        self.documents.extend(documents)

    # --------------------------------------------------
    # Query (same contract as Qdrant)
    # --------------------------------------------------
    def query_points(
        self,
        query: List[float],
        *,
        limit: int,
    ) -> VectorStore.QueryResponse:

        query_vec = np.asarray(query, dtype="float32")[None, :]

        if self.config.normalize:
            faiss.normalize_L2(query_vec)
        if self.index is None:
            raise ValueError(f"index should be created before querying points")
        scores, indices = self.index.search(query_vec, limit)

        points: List[VectorStore.ScoredPoint] = []

        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue
            points.append(
                VectorStore.ScoredPoint(
                    score=float(score),
                    document=self.documents[idx],
                )
            )
        return VectorStore.QueryResponse(points=points)


class QdrantVectorStore(VectorStore[QdrantVectorStoreSettings]):

    def __init__(self, config: QdrantVectorStoreSettings):
        super().__init__(config)
        self.client = QdrantClient(url=self.config.url)

    def query_points(self, query: List[float], *, limit: int) -> VectorStore.QueryResponse:
        result = self.client.query_points(
            collection_name=self.config.collection_name,
            query=query,
            limit=limit,
        )
        points: List[VectorStore.ScoredPoint] = []
        for idx, point in enumerate(result.points):
            payload = point.payload
            if payload is None:
                raise ValueError(
                    f"Qdrant returned a point with no payload | "
                    f"collection={self.config.collection_name} | "
                    f"index={idx} | score={point.score}"
                )
            if "page_content" not in payload:
                raise KeyError(
                    f"Missing 'page_content' in payload | "
                    f"collection={self.config.collection_name} | "
                    f"keys={list(payload.keys())}"
                )
            page_content = payload["page_content"]
            metadata = dict(payload["metadata"])
            points.append(
                VectorStore.ScoredPoint(
                    score=point.score,
                    document=Document(
                        page_content=page_content,
                        metadata=metadata,
                    ),
                )
            )

        return VectorStore.QueryResponse(points=points)
