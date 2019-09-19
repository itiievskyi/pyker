from typing import List
from pyker.generators import BaseGenerator

# wildcart import is to detect all generators so that be able to find BaseGenerator subclasses
from pyker.generators import *  # noqa: 403


def get_all_generators() -> List[BaseGenerator]:
    return BaseGenerator.__subclasses__()
