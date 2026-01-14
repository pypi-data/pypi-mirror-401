#!/usr/bin/env python

# SPDX-FileCopyrightText: 2025 wmj <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""General types."""

from __future__ import annotations
from typing import (
    Protocol,
    Hashable,
    TypeVar,
    Type,
    overload,
)
import warnings
import enum
from fractions import Fraction


class SortHash(Hashable, Protocol):
    """Sortable and hashable type."""

    def __lt__(self, value):  # type: ignore[no-untyped-def]
        """SortHash must have comparing methods."""


Score = int | Fraction
"A numerical type without precision loss."

FScore = Score | float
"A numerical type for integer, fractional or floating point."


def as_score(val: FScore) -> Score:
    """Convert a FScore to a Score."""
    if isinstance(val, (int, Fraction)):
        return val
    rval = int(val)
    if rval == val:
        return rval
    warnings.warn(
        "Floating point value converted to fraction. A precision loss may occur.", stacklevel=-1
    )
    fval = Fraction(val)
    if fval.denominator == 1:
        return fval.numerator
    return fval


_T = TypeVar("_T")


def ifnone(value: _T | None, default: _T) -> _T:
    """Return a non optional value from an optional value."""
    if value is None:
        value = default
    return value


def enum_from_string(value: str) -> str:
    """Convert a string to a canonical form for an enum attribute name."""
    return value.strip().replace(" ", "_").replace("-", "_").upper()


_Enum = TypeVar("_Enum", bound=enum.Enum)


def parse_enum(cls: Type[_Enum], value: str, canon: bool = True) -> _Enum:
    """Parse an attribute name for a Enum type."""
    if canon:
        value = enum_from_string(value)
    try:
        return cls[value]
    except KeyError as exc:
        raise ValueError(f"unknown value {value}") from exc


_Flag = TypeVar("_Flag", bound=enum.Flag)


def flag_from_string(value: str, sep: str) -> str:
    """Convert a string to a canonical form for a flag attribute name."""
    seps = [x for x in "|+,;" if x != sep]
    value = enum_from_string(value)
    for alt_sep in seps:
        value = value.replace(alt_sep, sep)
    return value


def parse_flag(cls: Type[_Flag], text: str, canon: bool = True, sep: str = "+") -> _Flag | None:
    """Parse an attribute name for a Flag type."""
    if canon:
        text = flag_from_string(text, sep)
    if not text:
        return None
    out: _Flag | None = None
    for value in text.split(sep):
        clean_value = value.strip()
        part: _Flag | None = None
        try:
            part = cls[clean_value]
        except KeyError as exc:
            raise ValueError(f"unknown value {value}") from exc
        if not out:
            out = part
        else:
            out |= part
    return out


@overload
def division(num: Score, den: Score) -> Score: ...


@overload
def division(num: float, den: FScore) -> int | float: ...


@overload
def division(num: FScore, den: float) -> int | float: ...


def division(num: FScore, den: FScore) -> FScore:
    """Make a fraction or a float division."""
    if isinstance(den, float) or isinstance(num, float):
        return num / den
    return Fraction(num, den)
