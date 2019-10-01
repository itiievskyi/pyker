import importlib
import re
from string import Template
from typing import Optional

from pyker.config import DEFAULT_LOCALE
from pyker.exceptions import PykerArgumentError, PykerLocalizationError
from pyker.generators import BaseGenerator


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

    def _create_template(self, structure) -> Template:
        gender = "male" if structure._male else "female"
        placeholders = [
            f"${attribute}_{gender}"
            for attribute in structure.__dir__()
            if getattr(structure, attribute) and not attribute.startswith("_")
        ]
        return Template(" ".join(placeholders))

    def _get_random_name(self, t: Template) -> str:
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
                    kwargs[key] = self.random_choice(getattr(self.data, key))
            except AttributeError:
                raise PykerLocalizationError(
                    f"`{key}` is unavailable for current locale: `{self.generator_locale}`"
                )
        return t.substitute(kwargs)

    def name(self, template: Optional[str] = None) -> str:
        if template:
            return self._get_random_name(Template(template))
        weights = [t._weight for t in self.data.templates]
        template = self.random.choices(self.data.templates, weights=weights, k=1)[0]
        string_template = self._create_template(template)
        return self._get_random_name(string_template)

