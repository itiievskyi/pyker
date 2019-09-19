from random import Random
import os, pkgutil

class BaseGenerator():
    
    def __init__(self, randomizer: Random):
        self.random = randomizer
    
    def random_element():
        pass

__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))