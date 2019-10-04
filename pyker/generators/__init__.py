import os
import pkgutil
import re
import string
from random import Random
from typing import Any, Iterable, List, Optional, Tuple, Union

from pyker.decorators import with_batch, with_sorted_batch
from pyker.exceptions import PykerArgumentError
from pyker.utils.get_subscriptable_object import get_subscriptable_object

MAX_INT = 1000000
MIN_INT = -MAX_INT

_re_hash = re.compile(r'#')


class BaseGenerator:
    def __init__(self, randomizer: Random, locale: str = "en_US"):
        from pyker.config import BATCH_LIMIT

        self.random = randomizer
        self.locale = locale
        self._batch_limit = BATCH_LIMIT

    def set_batch_limit(self, limit: int):
        """Sets the batch limit for the cases of random batch size"""
        if limit > 0:
            self._batch_limit = limit

    def _get_batch_size(self, start: int = 1, end: int = None) -> int:
        return self.random.randint(start, end or self._batch_limit)

    @with_sorted_batch
    def random_digit(self, without_zero: bool = False) -> Union[int, List[int]]:
        """
        Returns a random digit as integer (number).
        `0` (zero) can be excluded by setting `without_zero` to True.
        :param without_zero: should 0 be excluded from possible options?
        :returns: random digit (as integer), from 0 to 9 (or 1 to 9 if without_zero == True)
        """
        start_limit = int(without_zero)
        return self.random.randint(start_limit, 9)

    @with_sorted_batch
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

    @with_sorted_batch
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

    @with_batch
    def random_letter(self) -> Union[str, List[str]]:
        """Returns random letter from ASCII set (a-z plus A-Z)"""
        return self.random.choice(string.ascii_letters)

    @with_batch
    def random_uppercase_letter(self) -> Union[str, List[str]]:
        """Returns random uppercase letter from ASCII set (A-Z)"""
        return self.random.choice(string.ascii_uppercase)

    @with_batch
    def random_lowercase_letter(self) -> Union[str, List[str]]:
        """Returns random lowercase letter from ASCII set (a-z)"""
        return self.random.choice(string.ascii_lowercase)

    def random_choice(self, elements: Iterable[Any]) -> Any:
        """Returns random element from iterable object"""
        return self.random.choice(get_subscriptable_object(elements))

    def multiple_choice(
        self, elements: Iterable[Any], size: Optional[int] = None, unique: bool = False
    ) -> Iterable[Any]:
        """Returns a list containing several random elements from iterable object"""

        original_object = (
            get_subscriptable_object(elements)
            if not unique
            else set(get_subscriptable_object(elements))
        )
        object_length = len(original_object)
        new_size = size if size is not None else self.random.randint(0, object_length)

        try:
            return self.random.sample(original_object, new_size)
        except ValueError:
            raise PykerArgumentError(
                "Batch size cannot be negative or exceed the size of original object."
            )

    def random_sequence(
        self, elements: Iterable[Any], length: Optional[int] = None
    ) -> Iterable[Any]:
        """Returns a random sequence from iterable object"""

        original_object = get_subscriptable_object(elements)
        object_length = len(original_object)

        seq_length = (
            length if length is not None else self.random.randint(1, object_length)
        )

        if seq_length > object_length or seq_length < 1:
            raise PykerArgumentError(
                "Sequence size cannot be less than 1 or exceed the size of original object."
            )

        start = self.random.randint(0, object_length - seq_length)
        return original_object[start : start + seq_length]

    def shuffle_list(self, elements: List) -> List:
        """Shuffles elements of the list"""
        try:
            new_list = elements[:]  # creating a shallow copy of the list
            self.random.shuffle(elements)  # in-place shuffling
            return new_list
        except (KeyError, TypeError):
            raise PykerArgumentError("Only list can be used for shuffling.")

    def numerify(self, text: str) -> str:
        """Replaces all '#' occurences in the given string with random digits (0-9)"""
        return _re_hash.sub(
            lambda x: str(self.random_digit()),
            text)



# getting the list of generator module names for wildcard import
__all__ = list(
    module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)])
)
