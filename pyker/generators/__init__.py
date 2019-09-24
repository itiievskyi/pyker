import os
import pkgutil
from random import Random
from typing import Callable, List, Union


def with_batch(decorated: Callable) -> Callable:
    """Provides batch functionality for passed function (method)"""

    def wrapped(self, **kwargs):
        batch = kwargs.get("batch", False)
        if batch is True:
            return [decorated(self, **kwargs) for _ in range(self._get_batch_size())]
        elif batch > 0:
            return [decorated(self, **kwargs) for _ in range(batch)]
        return decorated(self, **kwargs)

    return wrapped


class BaseGenerator:
    def __init__(self, randomizer: Random):
        from pyker.config import BATCH_LIMIT

        self.random = randomizer
        self._batch_limit = BATCH_LIMIT

    def set_batch_limit(self, limit: int):
        """Sets the batch limit for the cases of random batch size"""
        if limit > 0:
            self._batch_limit = limit

    def _get_batch_size(self, limit: int = None) -> int:
        return self.random.randint(1, limit or self._batch_limit)

    @with_batch
    def random_digit(
        self, without_zero: bool = False, **kwargs
    ) -> Union[int, List[int]]:
        """
        Returns a random digit as integer (number).
        `0` (zero) can be excluded by setting `without_zero` to True.
        :param without_zero: should 0 be excluded from possible options?
        :returns: random digit (as integer), from 0 to 9 (or 1 to 9 if without_zero == True)
        """
        start_limit = int(without_zero)
        return self.random.randint(start_limit, 9)


# getting the list of generator module names for wildcard import
__all__ = list(
    module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)])
)
