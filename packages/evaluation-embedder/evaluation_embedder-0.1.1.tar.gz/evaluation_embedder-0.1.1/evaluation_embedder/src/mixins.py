from abc import ABC
from pathlib import Path
from typing import Any, Dict, Generic, Self, Type, get_args

import yaml

from evaluation_embedder.src.constants import TCFromConfigMixin
from evaluation_embedder.src.utils import load_class


class FromConfigMixin(ABC, Generic[TCFromConfigMixin]):

    def __init__(self, config: TCFromConfigMixin) -> None:
        super().__init__()
        self.config = config

    @classmethod
    def from_config(
        cls,
        config: TCFromConfigMixin,
    ) -> Self:
        return cls(config)

    @classmethod
    def get_config_class(cls) -> Type[TCFromConfigMixin]:
        return get_args(cls.__orig_bases__[0])[0]  # type: ignore

    @classmethod
    def from_yaml(
        cls,
        path: str,
        key: str | None = None,
    ) -> Self:
        """
        Load a runtime object from YAML.

        Args:
            yaml_path: Path to YAML config file
            settings_cls: Pydantic Settings model to validate config
            key: Optional top-level YAML key (e.g. "retriever")

        Returns:
            Instantiated runtime object
        """
        yaml_path = Path(path)
        with yaml_path.open("r") as f:
            raw: Dict[str, Any] = yaml.safe_load(f)
        if key is not None:
            raw = raw[key]
        settings = cls.get_config_class().model_validate(raw)
        runtime_cls = load_class(settings.module_path)
        return runtime_cls(settings)  # type: ignore[no-any-return]

    @classmethod
    def from_settings(cls) -> Self:
        """
        Load runtime object using Pydantic Settings resolution:
        init > yaml > env > dotenv > secrets
        """
        settings = cls.get_config_class()()  # type: ignore[call-arg]
        return load_class(settings.module_path)(settings)  # type: ignore[no-any-return]
