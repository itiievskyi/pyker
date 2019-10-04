import importlib
from string import Template
from typing import Any, List, Optional

from pyker.config import DEFAULT_LOCALE
from pyker.decorators import with_batch, with_sorted_batch
from pyker.exceptions import PykerArgumentError, PykerLocalizationError
from pyker.generators import BaseGenerator

from .config import CreditCard, CardFormat


class CreditCardGenerator(BaseGenerator):
    def generate_number(self, iin: str, length: int) -> str:
        """Generates card number based on given iin and adds valid check digit"""
        # generating number with given iin, random digits, but without check digit
        card_number = self.numerify(f"{iin}{'#' * (length - len(iin) - 1)}")

        # generating check_number
        evens = [(int(n) * 2 // 10 + int(n) * 2 % 10) for n in card_number[::2]]
        odds = [int(n) for n in card_number[1::2]]
        total = sum(evens + odds)
        check_digit = (10 - total % 10) % 10

        # adding check digit to card number
        card_number += str(check_digit)

        return card_number
