from pyker.config import GENERATORS
from pyker.randomizer import RandomMixin


class Pyker(RandomMixin, object):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__generators = GENERATORS

        for generator in GENERATORS:
            # for every generator list all methods
            # and set them as callable public methods of Pyker instance
            generator = generator(self.random)
            for method_name in dir(generator):
                # skip 'private' methods
                if method_name.startswith("_"):
                    continue

                pyker_method = getattr(generator, method_name)

                if callable(pyker_method):
                    setattr(self, method_name, pyker_method)
