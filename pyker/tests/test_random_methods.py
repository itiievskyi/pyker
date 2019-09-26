import pytest

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
