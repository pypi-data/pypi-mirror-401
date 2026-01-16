from typing import Generic, List

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from evaluation_embedder.src.constants import (
    CONFIG_PATH,
    FAISSIndexType,
    TCDataset,
    TCEmbedder,
    TCProcessor,
    TCRetriever,
    TCScore,
    TCVectorStore,
)


class DatasetSettings(BaseSettings):
    module_path: str


class ParquetDatasetSettings(DatasetSettings):
    path: str
    lazy: bool


class MinioDatasetSettings(DatasetSettings):
    endpoint: str
    bucket: str
    key: str
    access_key: str
    secret_key: str
    model_config = SettingsConfigDict(env_prefix='MINIO_', extra="ignore")


class FromConfigMixinSettings(BaseSettings):
    module_path: str
    model_config = SettingsConfigDict(
        yaml_file=CONFIG_PATH,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


class EmbedderSettings(FromConfigMixinSettings):
    model_name: str


class VLLMEmbedderSettings(EmbedderSettings):
    base_url: str


class ProcessorSettings(FromConfigMixinSettings):
    pass


class NomicProcessorSettings(ProcessorSettings):
    pass


class ScoreSettings(BaseSettings):
    module_path: str


class RecallAtKScoreSettings(ScoreSettings):
    k: int


class PrecisionAtKScoreSettings(ScoreSettings):
    k: int


class HitAtKScoreSettings(ScoreSettings):
    k: int


class MRRAtKScoreSettings(ScoreSettings):
    k: int


class VectorStoreSettings(FromConfigMixinSettings):
    pass


class QdrantVectorStoreSettings(VectorStoreSettings):
    url: str
    collection_name: str


class FaissVectorStoreSettings(VectorStoreSettings):
    index_type: FAISSIndexType
    normalize: bool


class RetrieverSettings(FromConfigMixinSettings, Generic[TCEmbedder, TCVectorStore, TCProcessor]):
    embedder: TCEmbedder
    vector_store: TCVectorStore
    processor: TCProcessor


class EvaluatorSettings(FromConfigMixinSettings, Generic[TCDataset, TCRetriever, TCScore]):
    dataset: TCDataset
    retriever: TCRetriever
    scores: List[TCScore]


class QdrantEvaluatorSettings(
    EvaluatorSettings[
        MinioDatasetSettings,
        RetrieverSettings[VLLMEmbedderSettings, QdrantVectorStoreSettings, NomicProcessorSettings],
        RecallAtKScoreSettings,
    ]
):
    pass


class FaissEvaluatorSettings(
    EvaluatorSettings[
        MinioDatasetSettings,
        RetrieverSettings[VLLMEmbedderSettings, FaissVectorStoreSettings, NomicProcessorSettings],
        RecallAtKScoreSettings,
    ]
):
    pass
