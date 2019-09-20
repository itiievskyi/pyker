import random as py_random

random = py_random.Random()


class RandomMixin:
    def __init__(self):
        self.random = random
        self.batch_limit = 100

    def seed_instance(self, seed=None):
        """Calls random.seed"""
        if self.__random == random:
            self.__random = py_random.Random()
        self.__random.seed(seed)
        return self

    @classmethod
    def seed(cls, seed=None):
        random.seed(seed)

    def get_batch_size(self, limit: int = None) -> int:
        return self.random.randint(1, limit or self.batch_limit)
