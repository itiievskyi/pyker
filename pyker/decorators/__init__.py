from enum import Enum, unique
from typing import TYPE_CHECKING, Callable, Iterable, Optional, Tuple, Union

from pyker.exceptions import PykerArgumentError

if TYPE_CHECKING:
    from pyker.generators import BaseGenerator


@unique
class SortOrder(Enum):
    asc = False
    desc = True


def with_batch(decorated: Callable) -> Callable:
    """Provides batch functionality for passed function (method)"""

    def wrapped(
        self: "BaseGenerator",
        *args,
        batch: Union[bool, int, Tuple[int, int]] = False,
        **kwargs,
    ):
        if batch is True:
            return [
                decorated(self, *args, **kwargs) for _ in range(self._get_batch_size())
            ]
        elif type(batch) == int and batch > 0:
            return [decorated(self, *args, **kwargs) for _ in range(batch)]
        elif type(batch) == tuple:
            start, end = batch
            if start >= 0 and end > start:
                return [
                    decorated(self, *args, **kwargs)
                    for _ in range(self._get_batch_size(start=start, end=end))
                ]
        return decorated(self, *args, **kwargs)

    return wrapped


def with_sorting(decorated: Callable) -> Callable:
    """Provides sorting capabilities for functions that return iterable values"""

    def wrapped(
        self: "BaseGenerator", *args, sort_batch: Optional[SortOrder] = None, **kwargs
    ):
        result = decorated(self, *args, **kwargs)
        if isinstance(result, Iterable) and sort_batch is not None:
            try:
                return sorted(
                    decorated(self, *args, **kwargs),
                    reverse=SortOrder[sort_batch].value,
                )
            except KeyError:
                raise PykerArgumentError(
                    "`sort_batch` should be either `asc` or `desc`."
                )
        return decorated(self, *args, **kwargs)

    return wrapped


def with_sorted_batch(decorated: Callable) -> Callable:
    """Combines `with_batch` and `with_sorting` decorators"""
    return with_sorting(with_batch(decorated))
