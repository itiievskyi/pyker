from dataclasses import dataclass
from string import Template


@dataclass
class PersonName:
    _male: bool
    _weight: int = 1

    prefix: bool = False
    first_name: bool = True
    middle_name: bool = False
    last_name: bool = True
    suffix: bool = False


templates_male = [
    PersonName(_male=True, first_name=True, last_name=True, _weight=25),
    PersonName(_male=True, prefix=True, first_name=True, last_name=True),
    PersonName(_male=True, prefix=True, first_name=True, last_name=True, suffix=True),
    PersonName(_male=True, first_name=True, last_name=True, suffix=True),
    PersonName(
        _male=True, first_name=True, middle_name=True, last_name=True, _weight=5
    ),
    PersonName(
        _male=True, prefix=True, first_name=True, middle_name=True, last_name=True
    ),
    PersonName(
        _male=True,
        prefix=True,
        first_name=True,
        middle_name=True,
        last_name=True,
        suffix=True,
    ),
    PersonName(
        _male=True, first_name=True, middle_name=True, last_name=True, suffix=True
    ),
]

templates_female = [
    PersonName(_male=False, first_name=True, last_name=True, _weight=25),
    PersonName(_male=False, prefix=True, first_name=True, last_name=True),
    PersonName(_male=False, prefix=True, first_name=True, last_name=True, suffix=True),
    PersonName(_male=False, first_name=True, last_name=True, suffix=True),
    PersonName(
        _male=False, first_name=True, middle_name=True, last_name=True, _weight=5
    ),
    PersonName(
        _male=False, prefix=True, first_name=True, middle_name=True, last_name=True
    ),
    PersonName(
        _male=False,
        prefix=True,
        first_name=True,
        middle_name=True,
        last_name=True,
        suffix=True,
    ),
    PersonName(
        _male=False, first_name=True, middle_name=True, last_name=True, suffix=True
    ),
]

templates = [*templates_male, *templates_female]

first_name_male = ["John", "Kevin"]
last_name_male = ["Smith", "Simpson"]
middle_name_male = first_name_male
suffix_male = ["Jr.", "II", "III", "PhD"]
prefix_male = ["Sir", "Mr."]

first_name_female = ["Sara", "Amy"]
last_name_female = ["Connor", "Scott"]
middle_name_female = first_name_female
suffix_female = ["MD", "PhD"]
prefix_female = ["Miss", "Mrs."]
