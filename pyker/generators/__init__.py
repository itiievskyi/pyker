from random import Random
from typing import Callable, List, Union
import os
import pkgutil


class BaseGenerator:
    def __init__(self, randomizer: Random):
        self.random = randomizer
        self.batch_limit = 100

    def set_batch_limit(self, limit: int):
        """Sets the batch limit for the cases of random batch size"""
        if limit > 0:
            self.batch_limit = limit

    def __get_batch_size(self, limit: int = None) -> int:
        return self.random.randint(1, limit or self.batch_limit)

    def __create_batch(
        self, f: Callable, batch: Union[int, bool] = False
    ) -> Union[int, List[int]]:
        if batch is True:
            return [f() for _ in range(self.__get_batch_size())]
        elif batch > 0:
            return [f() for _ in range(batch)]
        return f()

    def random_digit(
        self, without_zero: bool = False, batch: Union[int, bool] = False
    ) -> Union[int, List[int]]:
        """
        Returns a random digit as integer (number).
        `0` (zero) can be excluded by setting `without_zero` to True.
        :param without_zero: should 0 be excluded from possible options?
        :returns: random digit (as integer), from 0 to 9 (or 1 to 9 if without_zero == True)
        """
        start_limit = int(without_zero)
        return self.__create_batch(lambda: self.random.randint(start_limit, 9), batch)


# getting the list of generator module names for wildcard import
__all__ = list(
    module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)])
)
