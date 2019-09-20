from random import Random
from typing import List, Union
import os
import pkgutil


class BaseGenerator:
    def __init__(self, randomizer: Random):
        self.random = randomizer

    def random_element():
        pass

    def random_digit(self, without_zero: bool = False, batch: Union[int, bool] = False) -> Union[int, List[int]]:
        """
        Returns a random digit as integer (number).
        `0` (zero) can be excluded by setting `without_zero` to True.
        :param without_zero: should 0 be excluded from possible options?
        :returns: random digit (as integer), from 0 to 9 (or 1 to 9 if without_zero == True)
        """
        start_limit = int(without_zero)
        if batch == True:
            return [self.random.randint(start_limit, 9) for _ in range(self.get_batch_size())]
        elif batch > 0:
            return [self.random.randint(start_limit, 9) for _ in range(self.get_batch_size())]
        return self.random.randint(start_limit, 9)


# getting the list of generator module names for wildcard import
__all__ = list(
    module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)])
)
