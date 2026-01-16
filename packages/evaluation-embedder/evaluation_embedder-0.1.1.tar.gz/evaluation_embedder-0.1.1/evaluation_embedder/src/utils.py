import importlib
from typing import Any


def load_class(path: str) -> Any:
    module_path, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
