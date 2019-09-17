import pkgutil
from importlib import import_module
from typing import List

from pyker import generators


def get_module_names() -> List[str]:
    return [
        name
        for _, name, is_pkg in pkgutil.walk_packages(path=generators.__path__)
        if is_pkg
    ]


def get_all_modules(path: str):
    module_names = get_module_names()
    return set([import_module(f"{path}.{name}") for name in module_names])
