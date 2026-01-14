#!/usr/bin/env python

# SPDX-FileCopyrightText: 2025 wmj <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Preferential methods common code."""

from __future__ import annotations
from typing import (
    Sequence,
    Any,
    Iterable,
)

from ...types import Score
from ..types import (
    AnyName,
    AnotherName,
    Allocator,
    Data,
)
from ..types.preference import (
    Preference,
)


class PreferentialAllocator(Allocator[AnyName, Data]):
    """A preferential allocator."""

    # def __init__(self, input_type: Input):
    #     super().__init__(input_type | Input.PREFERENCES | Input.CANDIDATES)

    @staticmethod
    def get_max_ballot_size(data: Iterable[Preference[Any]]) -> int:
        """Return the size of the longest preference sequence."""
        return max(len(x.preference) for x in data)

    @staticmethod
    def _shrink_positions(votes: Sequence[Score]) -> Sequence[Score]:
        """Shrink positional votes from the end (less preferent).

        positions - candidate votes by positional preference
        """
        last_position = len(votes)
        for score in reversed(votes):
            if score > 0:
                break
            last_position -= 1

        return tuple(votes[:last_position])

    @classmethod
    def positional_votes(
        cls,
        data: Iterable[Preference[AnotherName]],
        ballot_size: int | None = None,
        whitelist: frozenset[AnotherName] | None = None,
        shrink: bool = True,
    ) -> tuple[dict[AnotherName, Sequence[Score]], int]:
        """Return positional votes by candidate."""
        if ballot_size is None:
            ballot_size = cls.get_max_ballot_size(data)

        # votes summed by a candidate by positional preferences
        scores: dict[AnotherName, list[Score]] = {}

        for batch in iter(data):
            if not batch.preference:
                continue

            for position, name in enumerate(batch.preference):
                assert not isinstance(name, (tuple, list))
                if (whitelist is not None) and (name not in whitelist):
                    continue
                if name not in scores:
                    scores[name] = [0] * ballot_size
                scores[name][position] += batch.votes

        if shrink:
            return {
                name: cls._shrink_positions(votes) for name, votes in scores.items()
            }, ballot_size
        return {name: tuple(votes) for name, votes in scores.items()}, ballot_size
