from pyker.generators import BaseGenerator


class PersonGenerator(BaseGenerator):
    def person_name(self):
        return self.random.randint(1, 20)
