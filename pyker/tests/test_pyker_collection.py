import pkgutil
import importlib
import sys
import inspect

from pyker import Pyker, generators
from pyker.generators import BaseGenerator


def test_method_collection():
    pyker = Pyker()

    # getting the list of user-defined methods available in Pyker instance
    instance_methods = set(
        [method for method in dir(pyker) if not method.startswith("_")]
    )

    # getting the list of methods that should be imported from all generators
    module_classes = set()  # to avoid extra inspections of BaseGenerator
    package_methods = (
        set()
    )  # to avoid duplicates (every Generator has methods from BaseGenerator)
    module_names = [
        name for _, name, is_pkg in pkgutil.iter_modules(path=generators.__path__)
    ]
    for module_name in module_names:
        module = importlib.import_module(f"pyker.generators.{module_name}")
        module_classes.update(
            dict(
                inspect.getmembers(
                    sys.modules[module.__name__],
                    lambda cls: inspect.isclass(cls) and issubclass(cls, BaseGenerator),
                )
            ).values()
        )

    for mod_class in module_classes:
        package_methods.update(
            [
                func
                for func in dir(mod_class)
                if callable(getattr(mod_class, func)) and not func.startswith("_")
            ]
        )

    # check if all user-defined methods found in `generators` package are available in Pyker instance
    assert package_methods.issubset(instance_methods)
