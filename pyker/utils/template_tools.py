from string import Template
from typing import List

from pyker.exceptions import PykerArgumentError


def get_template_keys(t: Template, possible_keys: List[str]) -> List[str]:
    """Returns list of automatically recognized placeholders from string Template without `$`"""
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

    for key in keys:
        if key not in possible_keys:
            raise PykerArgumentError(
                f"Invalid key: `{key}`. Available keys are: {possible_keys}."
            )

    return keys


def fill_template(template: Template, data: dict) -> str:
    """Checks placeholders for errors and returns string Template object"""
    try:
        return template.substitute(data)
    except ValueError:
        raise PykerArgumentError(
            f"Invalid template format. Use only valid string with placeholders of type `$<string>`.\
                Dollar sign should be escaped: `$$`."
        )
