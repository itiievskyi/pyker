from pyker.generators import BaseGenerator

class PersonGenerator(BaseGenerator):

    def person_name():
        return self.random.randint(1, 20)

__all__ = "PersonGenerator"