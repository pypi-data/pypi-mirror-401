from dataclasses import dataclass

from tdm.abstract.datamodel import AbstractValue
from tdm.abstract.datamodel.value import EnsureConfidenced
from tdm.abstract.json_schema import generate_model


@dataclass(frozen=True)
class _StringLocaleValue(EnsureConfidenced):
    """
    Auxiliary class for `StringLocaleValue` to fix dataclass fields order.

    Represents the internal structure of a `StringLocaleValue`.

    Attributes
    ----------
    str:
        Normalized string.
    locale:
        ISO 639-1 code standard.
    """
    str: str
    locale: str


@generate_model
@dataclass(frozen=True)
class StringLocaleValue(AbstractValue, _StringLocaleValue):
    """
    Represents a normalized KB value for string locale.
    """
    pass
