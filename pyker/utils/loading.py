from typing import List
import pkgutil
from pyker import generators
from importlib import import_module


def get_module_names(path: str) -> List[str]:
    return [
        name
        for _, name, is_pkg in pkgutil.walk_packages(path=generators.__path__)
        if is_pkg
    ]


def get_all_modules(path: str):
    module_names = get_module_names(path)
    return set([import_module(f"{path}.{name}") for name in module_names])
