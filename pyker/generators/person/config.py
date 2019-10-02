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
