import importlib
import re
from string import Template
from typing import Any, List, Optional

from pyker.config import DEFAULT_LOCALE
from pyker.decorators import with_batch, with_sorted_batch
from pyker.exceptions import PykerArgumentError, PykerLocalizationError
from pyker.generators import BaseGenerator
from .config import PersonName


class PersonGenerator(BaseGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.data = importlib.import_module(f"{__package__}.{self.locale}")
            self.generator_locale = self.locale
        except ModuleNotFoundError:
            try:
                self.data = importlib.import_module(f"{__package__}.{DEFAULT_LOCALE}")
                self.generator_locale = DEFAULT_LOCALE
            except ModuleNotFoundError:
                raise PykerLocalizationError(
                    f"Failed to load both `{self.locale}` and `{DEFAULT_LOCALE}` (default) locales."
                )

    def _create_name_template(self, templates: List[PersonName]) -> Template:
        """Chooses random template (based on weights) from given list and transformes it to string Template with placeholders."""
        weights = [t._weight for t in templates]
        structure = self.random.choices(templates, weights=weights, k=1)[0]
        gender = "male" if structure._male else "female"
        placeholders = [
            f"${attribute}_{gender}"
            for attribute in structure.__dir__()
            if getattr(structure, attribute) and not attribute.startswith("_")
        ]
        return Template(" ".join(placeholders))

    def _get_random_localized_attribute(self, key: str) -> Any:
        """Returns random element from localized data by key."""
        try:
            return self.random_choice(getattr(self.data, key))
        except AttributeError:
            raise PykerLocalizationError(
                f"`{key}` is unavailable for current locale: `{self.generator_locale}`"
            )

    def _get_random_name(self, t: Template) -> str:
        """Fills given string template with random elements from name parts (based on placeholders)."""
        try:
            keys = [group[1] for group in t.pattern.findall(t.template) if group[1]]
        except (StopIteration, IndexError):
            raise PykerArgumentError(
                f"Error. No valid placeholders found in template: {t.template}."
            )

        if not len(keys):
            raise PykerArgumentError(
                f"Error. No valid placeholders found in template: {t.template}."
            )

        kwargs = {}
        reserved_middle_name = ""
        for key in keys:
            try:
                if key.startswith("first_name"):
                    names = self.multiple_choice(
                        getattr(self.data, key), size=2, unique=True
                    )
                    kwargs[key] = names[0]
                    reserved_middle_name = names[1]
                elif key.startswith("middle_name") and getattr(
                    self.data, key
                ) == getattr(self.data, key.replace("middle", "first")):
                    kwargs[key] = reserved_middle_name
                else:
                    kwargs[key] = self._get_random_localized_attribute(key)
            except AttributeError:
                raise PykerLocalizationError(
                    f"`{key}` is unavailable for current locale: `{self.generator_locale}`"
                )
        return t.substitute(kwargs)

    @with_sorted_batch
    def name_from_template(template: str) -> str:
        """Creates random name based on given string template.
        For example, template `$prefix $first_name $last_name` will be filled with random elements from `prefix`, `first_name` and `last_name` lists.
        """
        return self._get_random_name(Template(template))
    
    @with_sorted_batch
    def name(self) -> str:
        """Creates random name. Includes only first name and last name."""
        templates_to_choose = [t for t in self.data.templates if (not t.prefix and not t.middle_name and not t.suffix)]
        string_template = self._create_name_template(templates_to_choose)
        return self._get_random_name(string_template)
    
    @with_sorted_batch
    def name_male(self) -> str:
        """Creates random male name. Includes only first name and last name."""
        templates_to_choose = [t for t in self.data.templates_male if (not t.prefix and not t.middle_name and not t.suffix)]
        string_template = self._create_name_template(templates_to_choose)
        return self._get_random_name(string_template)
    
    @with_sorted_batch
    def name_female(self) -> str:
        """Creates random female name. Includes only first name and last name."""
        templates_to_choose = [t for t in self.data.templates_female if (not t.prefix and not t.middle_name and not t.suffix)]
        string_template = self._create_name_template(templates_to_choose)
        return self._get_random_name(string_template)

    @with_batch
    def full_name(self) -> str:
        """Creates random name. First name and last name are guaranteed, prefix, middle name and suffix are optional."""
        string_template = self._create_name_template(self.data.templates)
        return self._get_random_name(string_template)

    @with_batch
    def full_name_male(self) -> str:
        """Creates random male name. First name and last name are guaranteed, prefix, middle name and suffix are optional."""
        string_template = self._create_name_template(self.data.templates_male)
        return self._get_random_name(string_template)

    @with_batch
    def full_name_female(self) -> str:
        """Creates random female name. First name and last name are guaranteed, prefix, middle name and suffix are optional."""
        string_template = self._create_name_template(self.data.templates_female)
        return self._get_random_name(string_template)

    @with_sorted_batch
    def first_name(self) -> str:
        """Returns random first name."""
        return self._get_random_localized_attribute('first_name')

    @with_sorted_batch
    def first_name_male(self) -> str:
        """Returns random male first name."""
        return self._get_random_localized_attribute('first_name_male')

    @with_sorted_batch
    def first_name_female(self) -> str:
        """Returns random female first name."""
        return self._get_random_localized_attribute('first_name_female')

    @with_sorted_batch
    def last_name(self) -> str:
        """Returns random last name."""
        return self._get_random_localized_attribute('last_name')

    @with_sorted_batch
    def last_name_male(self) -> str:
        """Returns random male last name."""
        return self._get_random_localized_attribute('last_name_male')

    @with_sorted_batch
    def last_name_female(self) -> str:
        """Returns random female last name."""
        return self._get_random_localized_attribute('last_name_female')

    @with_sorted_batch
    def middle_name(self) -> str:
        """Returns random last name."""
        return self._get_random_localized_attribute('middle_name')

    @with_sorted_batch
    def middle_name_male(self) -> str:
        """Returns random male last name."""
        return self._get_random_localized_attribute('middle_name_male')

    @with_sorted_batch
    def middle_name_female(self) -> str:
        """Returns random female last name."""
        return self._get_random_localized_attribute('middle_name_female')

    @with_sorted_batch
    def prefix(self) -> str:
        """Returns random name prefix."""
        return self._get_random_localized_attribute('prefix')

    @with_sorted_batch
    def prefix_male(self) -> str:
        """Returns random male name prefix."""
        return self._get_random_localized_attribute('prefix_male')

    @with_sorted_batch
    def prefix_female(self) -> str:
        """Returns random female name prefix."""
        return self._get_random_localized_attribute('prefix_female')

    @with_sorted_batch
    def suffix(self) -> str:
        """Returns random name suffix."""
        return self._get_random_localized_attribute('suffix')

    @with_sorted_batch
    def suffix_male(self) -> str:
        """Returns random male name suffix."""
        return self._get_random_localized_attribute('suffix_male')

    @with_sorted_batch
    def suffix_female(self) -> str:
        """Returns random female name suffix."""
        return self._get_random_localized_attribute('suffix_female')
