from typing import Any, Dict, Iterable, Optional, Set

from pyker.exceptions import PykerArgumentError


def get_subscriptable_object(elements: Iterable[Any]) -> Optional[Iterable]:
    """Returns properly subscriptable object or raises an exception if initial object is invalid"""
    if not elements or not isinstance(elements, Iterable):
        raise PykerArgumentError(
            "Error during iterating. You can use only iterable non-empty object."
        )
    elif isinstance(elements, Dict):
        return list(elements.items())
    elif isinstance(elements, Set):
        return list(elements)
    return elements
