#!/usr/bin/env python

# SPDX-FileCopyrightText: 2025 wmj <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""A poor man's data frame."""

from __future__ import annotations
from typing import (
    Iterator,
)
from typing_extensions import override

from . import Bidimensional, AnyValue, AnyKey


class DataFrame(Bidimensional[AnyKey, int, AnyValue]):
    """Table for series of data."""

    def __init__(self) -> None:
        """Create an empty data frame."""
        self._data: dict[AnyKey, list[AnyValue]] = {}

    @override
    def empty(self) -> bool:
        return not self._data

    @override
    def row_size(self) -> int:
        return len(self._data)

    @override
    def col_size(self) -> int:
        return max(len(x) for x in self._data.values())

    @override
    def __getitem__(self, idx: tuple[AnyKey, int]) -> AnyValue:
        row, col = idx
        return self._data[row][col]

    @override
    def __setitem__(self, idx: tuple[AnyKey, int], value: AnyValue) -> None:
        row, col = idx
        self._data[row][col] = value

    @override
    def iter_row(self, row: AnyKey, sparse: bool = False) -> Iterator[tuple[int, AnyValue]]:
        return enumerate(self._data[row])

    @override
    def iter_col(self, col: int, sparse: bool = False) -> Iterator[tuple[AnyKey, AnyValue]]:
        for row, series in self._data.items():
            try:
                yield (row, series[col])
            except IndexError:
                pass

    @override
    def iter_row_keys(self) -> Iterator[AnyKey]:
        return iter(self._data.keys())

    @override
    def iter_col_keys(self) -> Iterator[int]:
        return iter(range(0, self.col_size()))

    @override
    def remove_row(self, row: AnyKey) -> None:
        del self._data[row]

    def insert_row(self, row: AnyKey, series: list[AnyValue]) -> None:
        """Insert or replace a row."""
        self._data[row] = series
