import importlib
import pytest

from pyker import Pyker
from pyker.exceptions import PykerArgumentError
from pyker.generators.person.config import POSSIBLE_KEYS
from pyker.generators.person.en_US import (
    first_name,
    first_name_female,
    last_name,
    prefix,
)


class TestPerson:
    pyker = Pyker()

    @pytest.mark.parametrize("batch", [100])
    def test_regular_name(self, batch):
        # single name: first name + last name
        name = self.pyker.name()
        parts = name.split()
        assert parts[0] in first_name and parts[1] in last_name

        # batch of names
        names = self.pyker.name(batch=batch)
        assert len(names) == batch
        assert all([len(name.split()) == 2 for name in names])

    @pytest.mark.parametrize("batch", [100])
    def test_full_name(self, batch):
        names = self.pyker.full_name(batch=batch)
        assert len(names) == batch
        assert all(
            [len(name.split()) >= 2 and len(name.split()) <= 5 for name in names]
        )

    @pytest.mark.parametrize("batch", [100])
    def test_name_with_gender(self, batch):
        names = self.pyker.name_female(batch=batch)
        assert len(names) == batch
        assert all([name.split()[0] in first_name_female for name in names])

    @pytest.mark.parametrize("batch", [100])
    def test_name_template(self, batch):
        name = self.pyker.name_from_template("$prefix $first_name $last_name")
        parts = name.split()
        assert len(parts) == 3
        assert parts[0] in prefix and parts[1] in first_name and parts[2] in last_name

        # preserving non-placeholders
        name = self.pyker.name_from_template(
            "My name is $prefix $first_name $last_name"
        )
        assert name.startswith("My name is")
        assert len(name.split()) == 6

    def test_name_template_errors(self):
        # no placeholders
        with pytest.raises(PykerArgumentError):
            assert self.pyker.name_from_template("Hi! I'm ...")

        # wrong placeholder - `$surname`
        with pytest.raises(PykerArgumentError):
            assert self.pyker.name_from_template("$last_name $surname")

        # incosistent placeholders (with gender and without)
        with pytest.raises(PykerArgumentError):
            assert self.pyker.name_from_template("$last_name $first_name_male")

        # invalid placeholder format for $100
        with pytest.raises(PykerArgumentError):
            assert self.pyker.name_from_template("$first_name_male gave me $100")
        assert self.pyker.name_from_template("$first_name_male gave me $$100")

    def test_middle_name(self):
        # for languages where middle name has the same form as first name
        # they shouldn't be equal
        names_parts = [
            name.split()
            for name in self.pyker.name_from_template(
                "$first_name $middle_name", batch=1000
            )
        ]
        assert all([parts[0] != parts[1] for parts in names_parts])

    def test_name_parts(self):
        localized = importlib.import_module(f"pyker.generators.person.en_US")
        # it checks every name part such as first name, last name, prefix, etc.
        # calling three methods each part (_male, _female and without gender prefix)
        for key in POSSIBLE_KEYS:
            name_part = getattr(self.pyker, key)()
            assert len(name_part.split()) == 1
            assert getattr(self.pyker, key)() in getattr(localized, key)
