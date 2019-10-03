from dataclasses import dataclass


@dataclass
class PersonName:
    _male: bool
    _weight: int = 1

    prefix: bool = False
    first_name: bool = True
    middle_name: bool = False
    last_name: bool = True
    suffix: bool = False


# Possible name "parts" that could be used as template keys and imported from localized module
POSSIBLE_KEYS = [
    "first_name_male",
    "last_name_male",
    "middle_name_male",
    "suffix_male",
    "prefix_male",
    "first_name_female",
    "last_name_female",
    "middle_name_female",
    "suffix_female",
    "prefix_female",
    "first_name",
    "last_name",
    "middle_name",
    "prefix",
    "suffix",
]
