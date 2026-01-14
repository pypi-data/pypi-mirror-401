from __future__ import annotations

import copy
from collections.abc import Mapping
from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


log = getLogger(__name__)


def dict_get_any(dikt: dict[str, Any], *names: str, fail: bool = True, default: Any | None = None) -> Any | None:
    """
    Return the value for the first matching key from a dictionary.

    :param dikt: Dictionary to search in.
    :param names: Candidate keys to look for (checked in order).
    :param fail: If True, raise KeyError if no key is found.
    :param default: Value to return if no key is found and fail=False.
    :return: The value from the first found key, or `default` if not found.
    :raises KeyError: If fail=True and no key is found.
    """
    key = next((name for name in names if name in dikt), None)
    if key is not None:
        return dikt[key]

    if fail:
        raise KeyError(f"Did not find one of the required keys: {names}. Possibly check the correct spelling.")
    return default


def dict_pop_any(dikt: dict[str, Any], *names: str, fail: bool = True, default: Any | None = None) -> Any | None:
    """
    Pop the first matching key from a dictionary.

    Removes and returns the value of the first key in `names` found in `dikt`.

    :param dikt: Dictionary to pop values from.
    :param names: Candidate keys to look for.
    :param fail: If True, raise KeyError if no key is found.
    :param default: Value to return if no key is found and fail=False.
    :return: The value from the first found key, or `default` if not found.
    :raises KeyError: If fail=True and no key is found.
    """
    key = next((name for name in names if name in dikt), None)
    if key is not None:
        return dikt.pop(key)

    if fail:
        raise KeyError(f"Did not find one of the required keys: {names}")
    return default


def dict_search(dikt: dict[str, str], val: str) -> str:
    """Get key of _psr_types dictionary, given value.

    Raise ValueError in case of value not specified in data.

    :param dikt: dictionary to search for value
    :param val: value to search
    :return: key of the dictionary
    """
    try:
        return next(key for key, value in dikt.items() if value == val)
    except StopIteration:
        raise ValueError(f"Value '{val}' not found in specified dictionary") from None


def deep_mapping_update(
    source: Any, overrides: Mapping[str, str | Mapping[str, Any]]
) -> dict[str, str | Mapping[str, Any]]:
    """Perform a deep update of a nested dictionary or similar mapping.

    :param source: Original mapping to be updated.
    :param overrides: Mapping with new values to integrate into the new mapping.
    :return: New Mapping with values from the source and overrides combined.
    """
    output = copy.deepcopy(source) if source else {}

    for key, value in overrides.items():
        if isinstance(value, Mapping):
            output[key] = deep_mapping_update(
                output.get(key, {}),  # merge into existing nested dict
                value,
            )
        else:
            output[key] = value

    return dict(output)


def camel_to_snake_case(camel_name: str) -> str:
    """Convert a string from camel to snake case convention"""
    return "".join("_" + c.lower() if c.isupper() else c for c in camel_name).strip("_")
