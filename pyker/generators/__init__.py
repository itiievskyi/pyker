import os
import pkgutil
from random import Random
from typing import Callable, List, Tuple, Union
from pyker.exceptions import PykerArgumentError

MAX_INT = 1000000
MIN_INT = -MAX_INT


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


class BaseGenerator:
    def __init__(self, randomizer: Random):
        from pyker.config import BATCH_LIMIT

        self.random = randomizer
        self._batch_limit = BATCH_LIMIT

    def set_batch_limit(self, limit: int):
        """Sets the batch limit for the cases of random batch size"""
        if limit > 0:
            self._batch_limit = limit

    def _get_batch_size(self, start: int = 1, end: int = None) -> int:
        return self.random.randint(start, end or self._batch_limit)

    @with_batch
    def random_digit(self, without_zero: bool = False) -> Union[int, List[int]]:
        """
        Returns a random digit as integer (number).
        `0` (zero) can be excluded by setting `without_zero` to True.
        :param without_zero: should 0 be excluded from possible options?
        :returns: random digit (as integer), from 0 to 9 (or 1 to 9 if without_zero == True)
        """
        start_limit = int(without_zero)
        return self.random.randint(start_limit, 9)

    @with_batch
    def random_number(
        self,
        without_negative: bool = False,
        limits: Tuple[int, int] = (MIN_INT, MAX_INT),
    ) -> Union[int, List[int]]:
        start, end = limits
        if start >= end:
            raise PykerArgumentError(f"Start point should be smaller than end limit")
        start_limit = 0 if start < 0 and without_negative else start
        return self.random.randint(start_limit, end)

    @with_batch
    def random_number_of_length(self, length: int) -> Union[int, List[int]]:
        """Returns random positive integer of fixed length"""
        if length < 1:
            raise PykerArgumentError(
                f"Argument `length` accepts only positive numbers, but `{length}` was provided."
            )
        if length == 1:
            return self.random_digit()
        elif length > 1:
            return self.random.randint(pow(10, length - 1), pow(10, length) - 1)


# getting the list of generator module names for wildcard import
__all__ = list(
    module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)])
)
