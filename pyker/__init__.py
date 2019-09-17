import random as py_random

from pyker.config import FAKERS

random = py_random.Random()


class Pyker(object):

    __config = {}

    def __init__(self, **config):
        self.__random = random
        self.fakers = FAKERS

        for faker in FAKERS:
            # for every faker (provider) list all methods
            # and set them as callable public methods of Pyker instance

            for method_name in dir(faker):
                # skip 'private' methods
                if method_name.startswith("_"):
                    continue

                pyker_method = getattr(faker, method_name)

                if callable(pyker_method):
                    setattr(self, method_name, pyker_method)
