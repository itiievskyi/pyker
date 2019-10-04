from dataclasses import dataclass
from typing import List


@dataclass
class CreditCard:
    number: str
    provider: str
    exp_date: str
    cvv: str
    cardholder: str


@dataclass
class CardFormat:
    provider: str
    codes: List[str]

    length: int = 16
    weight: int = 1


CARD_FORMATS = [
    CardFormat(provider="Visa", weight=10, codes=["4"]),
    CardFormat(provider="Visa", weight=1, codes=["4"], length=19),
]
