import random as py_random

random = py_random.Random()


class RandomMixin:
    def __init__(self):
        self.random = random

    def seed_instance(self, seed=None):
        """Calls random.seed"""
        if self.__random == random:
            self.__random = py_random.Random()
        self.__random.seed(seed)
        return self

    @classmethod
    def seed(cls, seed=None):
        random.seed(seed)
