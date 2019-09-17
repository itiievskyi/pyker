import random as py_random

from pyker.config import GENERATORS

random = py_random.Random()


class Pyker(object):

    __config = {}

    def __init__(self, **config):
        self.__random = random
        self.generators = GENERATORS

        for generator in GENERATORS:
            # for every generator (provider) list all methods
            # and set them as callable public methods of Pyker instance
            for method_name in dir(generator):
                # skip 'private' methods
                if method_name.startswith("_"):
                    continue

                pyker_method = getattr(generator, method_name)

                if callable(pyker_method):
                    setattr(self, method_name, pyker_method)

    @property
    def random(self):
        return self.__random

    @random.setter
    def random(self, value):
        self.__random = value

    def seed_instance(self, seed=None):
        """Calls random.seed"""
        if self.__random == random:
            self.__random = py_random.Random()
        self.__random.seed(seed)
        return self

    @classmethod
    def seed(cls, seed=None):
        random.seed(seed)
