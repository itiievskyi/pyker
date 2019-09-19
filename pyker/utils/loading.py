from typing import List

from pyker.generators import *
from pyker.generators import BaseGenerator

def get_all_generators() -> List[BaseGenerator]:
    return BaseGenerator.__subclasses__()
