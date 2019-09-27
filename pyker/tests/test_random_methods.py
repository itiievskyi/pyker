import pytest
import string

from pyker import Pyker
from pyker.exceptions import PykerArgumentError
from pyker.generators import MAX_INT, MIN_INT


class TestRandomMethods:
    pyker = Pyker()

    @pytest.mark.parametrize("number_of_tests", [100])
    def test_random_digit(self, number_of_tests):
        digits_with_zero = [self.pyker.random_digit() for _ in range(number_of_tests)]
        assert all(digit >= 0 and digit < 10 for digit in digits_with_zero)
        digits_without_zero = [
            self.pyker.random_digit(without_zero=True) for _ in range(number_of_tests)
        ]
        assert all(digit > 0 and digit < 10 for digit in digits_without_zero)

    @pytest.mark.parametrize("batch, limits", [(1000, (500, 1500))])
    def test_random_number(self, batch, limits):
        # single number
        number = self.pyker.random_number()
        assert isinstance(number, int)
        assert number >= MIN_INT and number <= MAX_INT
        # checking default limits for batch
        numbers = self.pyker.random_number(batch=batch)
        assert all(number >= MIN_INT and number <= MAX_INT for number in numbers)
        # checking negative numbers smart skipping
        positive_numbers = self.pyker.random_number(batch=batch, without_negative=True)
        assert min(positive_numbers) >= 0
        # checking custom limits
        custom_numbers = self.pyker.random_number(batch=batch, limits=limits)
        assert all(
            number >= limits[0] and number <= limits[1] for number in custom_numbers
        )
        # testing some errors
        with pytest.raises(PykerArgumentError):
            assert self.pyker.random_number(limits=(limits[0], -limits[1]))

    @pytest.mark.parametrize("batch, length", [(3, 100), (100, 3)])
    def test_random_number_of_length(self, batch, length):
        # single number
        number = self.pyker.random_number_of_length(length)
        assert isinstance(number, int)
        assert number > pow(10, length - 1) - 1
        # batch
        numbers = self.pyker.random_number_of_length(length, batch=batch)
        assert all(len(str(number)) == length for number in numbers)
        # testing exception for negative length
        with pytest.raises(PykerArgumentError):
            assert self.pyker.random_number_of_length(-10)

    @pytest.mark.parametrize("batch", [100])
    def test_random_letters(self, batch):
        # single letter
        assert self.pyker.random_letter() in string.ascii_letters
        assert self.pyker.random_uppercase_letter() in string.ascii_uppercase
        assert self.pyker.random_lowercase_letter() in string.ascii_lowercase

        # batch
        assert set(self.pyker.random_letter(batch=batch)).issubset(
            set(string.ascii_letters)
        )
        assert set(self.pyker.random_uppercase_letter(batch=batch)).issubset(
            set(string.ascii_uppercase)
        )
        assert set(self.pyker.random_lowercase_letter(batch=batch)).issubset(
            set(string.ascii_lowercase)
        )

    def test_random_choice(self):
        # single element
        assert self.pyker.random_choice("abc") in "abc"
        assert self.pyker.random_choice(set([1, 3, 5, 7, 1, 4, 3])) in [
            1,
            3,
            5,
            7,
            1,
            4,
            3,
        ]
        assert self.pyker.random_choice([1, 2, "str", True]) in [1, 2, "str", True]
        assert self.pyker.random_choice((1, 2, 3)) in (1, 2, 3)
        assert (
            self.pyker.random_choice({1: "a", 2: "b", 3: "c"})
            in {1: "a", 2: "b", 3: "c"}.items()
        )

        # exceptions
        with pytest.raises(PykerArgumentError):
            assert self.pyker.random_choice(10)  # number is not iterable
        with pytest.raises(PykerArgumentError):
            assert self.pyker.random_choice("")  # empty sequence
        with pytest.raises(PykerArgumentError):
            assert self.pyker.random_choice([])  # empty sequence

    def test_multiple_choice(self):
        original_list = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 1, 2, 4]

        random_list = self.pyker.multiple_choice(original_list)
        assert isinstance(random_list, list)
        assert len(random_list) <= len(original_list)

        fixed_size_list = self.pyker.multiple_choice(original_list, size=5)
        assert len(fixed_size_list) == 5

        unique_list = self.pyker.multiple_choice(original_list, unique=True)
        assert len(unique_list) == len(set(unique_list))

        # exceptions
        with pytest.raises(PykerArgumentError):
            assert self.pyker.multiple_choice(original_list, -2)  # negative batch size
        with pytest.raises(PykerArgumentError):
            assert self.pyker.multiple_choice(
                original_list, len(original_list) + 1
            )  # batch size > original size
        with pytest.raises(PykerArgumentError):
            assert self.pyker.multiple_choice([])  # empty sequence
