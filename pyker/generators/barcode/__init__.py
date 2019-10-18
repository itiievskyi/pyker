from typing import List, Optional

from pyker.data.countries import COUNTRIES, GS1

# from pyker.decorators import with_batch, with_sorted_batch
from pyker.exceptions import PykerArgumentError
from pyker.generators import BaseGenerator


class BarcodeGenerator(BaseGenerator):
    def _convert_prefix(self, prefix: int) -> List[int]:
        return [prefix // 100, prefix // 10 % 10, prefix % 10]

    def ean(self, length: int = 13, country: Optional[str] = None) -> str:
        if length not in (8, 13):
            raise PykerArgumentError("Length should be of length 8 or 13.")

        if country:
            try:
                prefix = self._convert_prefix(
                    self.random_choice(
                        [c.gs1 for c in COUNTRIES if c.alpha2 == country.lower()][0]
                    )
                )
            except IndexError:
                raise PykerArgumentError(
                    f"Wrong country code: `{country}`. Please use two-letter codes from ISO 3166-1 alpha-2."
                )
            except PykerArgumentError:
                raise PykerArgumentError(
                    f"No codes provided for country: `{country}`. Try using another one."
                )
        else:
            prefix = self._convert_prefix(self.random_choice(GS1))

        code = [
            *prefix,
            *[self.random_digit() for _ in range(length - len(prefix) - 1)],
        ]

        if length == 8:
            weights = [3, 1, 3, 1, 3, 1, 3]
        elif length == 13:
            weights = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]

        weighted_sum = sum(x * y for x, y in zip(code, weights))
        check_digit = (10 - weighted_sum % 10) % 10
        code.append(check_digit)

        return "".join(str(x) for x in code)
