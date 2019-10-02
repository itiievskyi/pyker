"""
Provide lists of name parts here:
    first_name_[male, female] = [...]
    last_name_[male, female] = [...]
    middle_name_[male, female] = [...]
    prefix_[male, female] = [...]
    suffix_[male, female] = [...]
"""

from ..config import PersonName
from string import Template

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


first_name_male = ["John", "Kevin"]
last_name_male = ["Smith", "Simpson"]
middle_name_male = first_name_male
suffix_male = ["Jr.", "II", "III", "PhD"]
prefix_male = ["Sir", "Mr."]

first_name_female = ["Sara", "Amy"]
last_name_female = last_name_male
middle_name_female = first_name_female
suffix_female = ["MD", "PhD"]
prefix_female = ["Miss", "Mrs."]


# combining male and female attribute lists
templates = [*templates_male, *templates_female]
first_name = [*first_name_male, *first_name_female]
last_name = [*last_name_male, *last_name_female]
middle_name = [*middle_name_male, *middle_name_female]
prefix = [*prefix_male, *prefix_female]
suffix = [*suffix_male, *suffix_female]
