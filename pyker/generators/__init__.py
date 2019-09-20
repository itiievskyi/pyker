from random import Random
import os
import pkgutil


class BaseGenerator:
    def __init__(self, randomizer: Random):
        self.random = randomizer

    def random_element():
        pass

    def random_digit(self, without_zero: bool = False) -> int:
        """
        Returns a random digit as integer (number).
        `0` (zero) can be excluded by setting `without_zero` to True.
        :param without_zero: should 0 be excluded from possible options?
        :returns: random digit (as integer), from 0 to 9 (or 1 to 9 if without_zero == True)
        """
        return self.random.randint(1, 9) if without_zero else self.random.randint(0, 9)


# getting the list of generator module names for wildcard import
__all__ = list(
    module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)])
)
