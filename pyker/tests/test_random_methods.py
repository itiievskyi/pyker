import pytest
from pyker import Pyker


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
