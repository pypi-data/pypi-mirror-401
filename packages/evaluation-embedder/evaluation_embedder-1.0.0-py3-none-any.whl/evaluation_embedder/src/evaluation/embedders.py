from typing import List

from evaluation_embedder.src.evaluation import Embedder
from evaluation_embedder.src.settings import VLLMEmbedderSettings
from openai import AsyncOpenAI


class VLLMEmbedder(Embedder[VLLMEmbedderSettings]):
    def __init__(self, config: VLLMEmbedderSettings):
        super().__init__(config)
        self.client = AsyncOpenAI(
            base_url=self.config.base_url,
            api_key="",  # vLLM does not require a key
        )

    async def _aembed(self, texts: List[str]) -> List[List[float]]:
        """
        Async embedding via vLLM OpenAI-compatible API.
        """
        response = await self.client.embeddings.create(
            model=self.config.model_name,
            input=texts,
        )

        # Preserve order
        return [item.embedding for item in response.data]
