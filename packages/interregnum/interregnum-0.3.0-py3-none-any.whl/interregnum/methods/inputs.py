#!/usr/bin/env python

# SPDX-FileCopyrightText: 2025 wmj <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Pre-defined arguments for `calc` methods in allocators."""

from __future__ import annotations
from typing import (
    Iterable,
    Generic,
    Sequence,
    Callable,
    TypeVar,
    Final,
)
from typing_extensions import TypedDict

from ..random import RandomSeed
from ..types import Score

from .types import AnyName, CandLike, AnyEvent, CandidateFilter
from .types.preference import PreferenceLike


PartyName = TypeVar("PartyName")
"Party name type"

DistrictName = TypeVar("DistrictName")
"District name type"

ICandidates = Iterable[CandLike[AnyName]]
"Iterable of candidate-like structures (name, votes)"

INames = Iterable[AnyName]
"Iterable of names"

IPreferences = Iterable[PreferenceLike[AnyName]]
"Iterable of preferences"

ISeats = Iterable[CandLike[AnyName]]
"Iterable of candidate-like structures (name, seats)"

INamedSeats = Iterable[tuple[AnyName, int]]
"Iterable of (name, seats)"

IConstraints = Sequence[tuple[int, Sequence[AnyName]]]
"Sequence of seats constraints (name1 + ... + nameN <= max seats)"

IPartyNameFunction = Callable[[AnyName], PartyName]
"A function that transforms a name to a party name"

IDistrictNameFunction = Callable[[AnyName], DistrictName]
"A function that transforms a name to a district name"

INameFunction = Callable[[tuple[PartyName, DistrictName]], AnyName]
"A function that create a name from a party name and a district name"


DEFAULT_SKIP_INITIAL_SEATS: Final[bool] = False


class InputDict(TypedDict, Generic[AnyName, AnyEvent], total=False):
    """Allowed allocator inputs."""

    random_seed: RandomSeed | None
    """A random generator seed.

    Examples
    --------

    a) Integer seed

        >>> inputs["random_seed"] = 42

    b) Random generator

        >>> inputs["random_seed"] = random.Random(42)
    """

    seats: int
    """Seats to allocate.

    Examples
    --------

    >>> inputs["seats"] = 64
    """

    candidates: ICandidates[AnyName]
    """List of candidates with names and votes.

    Examples
    --------

    a) two candidates (A: 200 votes; B: 150 votes)

        >>> inputs["candidates"] = [("A", 200), ("B", 150)]

    b) using the :class:`.types.Candidate` class

        >>> from interregnum.types import Candidate
        >>> inputs["candidates"] = [
        >>>    Candidate(name="A", votes=200),
        >>>    Candidate(name="B", votes=150),
        >>> ]
    """

    candidate_list: INames[AnyName]
    """Whole list of candidates.

    Examples
    --------

    >>> inputs["candidate_list"] = ["A", "B"]
    """

    preferences: IPreferences[AnyName]
    """Preferential votes ballots.

    Examples
    --------

    a) using tuples

        >>> inputs["preferences"] = [
        >>>     (200, ["A", "B", "C"]),
        >>>     (150, ["C", "B"])
        >>> ]

    b) using the :class:`.preferential.Preference`

        >>> from interregnum.preferential import Preference
        >>> inputs["preferences"] = Preference.make_input([
        >>>     (200, ["A", "B", "C"]),
        >>>     (150, ["C", "B"])
        >>> ])
    """

    party_seats: ISeats[AnyName]
    """Seats already allocated to parties.

    Examples
    --------

    >>> inputs["party_seats"] = [("P1", 10), ("P2", 8)]
    """

    district_seats: ISeats[AnyName]
    """Seats already allocated to districts.

    Examples
    --------

    >>> inputs["district_seats"] = [("D1", 20), ("D2", 15)]
    """

    initial_seats: INamedSeats[AnyName]
    """List of seats candidates have before the allocation.

    Examples
    --------

    >>> # A: 1, B: 2
    >>> inputs["initial_seats"] = [("A", 1), ("B", 2)]
    """

    inner_initial_seats: INamedSeats[AnyName]
    """List of seats candidates have before the allocation (used by adapters).

    Examples
    --------

    >>> # A: 1, B: 2
    >>> inputs["initial_seats"] = [("A", 1), ("B", 2)]
    """

    filter_f: CandidateFilter[AnyName, AnyEvent]
    """Filter function to exclude candidates from winning seats.

    Examples
    --------

    >>> # using a filter based on an exclusion list
    >>> from interregnum.methods.filters import ContenderSetFilter
    >>> # exclude candidates B and C
    >>> inputs["filter_f"] = ContenderSetFilter(["B", "C"])
    """

    total_votes: Score
    """Total number of tallied votes.

    Examples
    --------

    >>> inputs["total_votes"] = 12561
    """

    exclude_candidates: Iterable[AnyName]
    """List of candidates excluded from winning seats.

    Examples
    --------

    >>> inputs["exclude_candidates"] = ["B", "C"]
    """

    max_seats: int
    """Maximum number of seats that can be allocated.

    Examples
    --------

    >>> inputs["max_seats"] = 100
    """

    constraints: IConstraints[AnyName]
    """Seats constraints for groups of candidates.

    Examples
    --------

    >>> inputs["constraints"] = [
    >>>     # Mom from MomCorp is an independent candidate, so she can only win 1 seat
    >>>     (1, ["Mom"]),
    >>>     # the members of the alliance "Futurama" can only win 2 seats
    >>>     (2, ["Fry", "Leela", "Bender"]),
    >>> ]
    """

    max_ballots_size: int
    """Maximum size a ranked vote ballot can have.

    Examples
    --------

    >>> # 10 candidates can be selected on each ballot
    >>> inputs["max_ballots_size"] = 10
    """

    skip_initial_seats: bool
    """Do not include initial seats in the result."""


class BipropInputDict(
    InputDict[AnyName, AnyEvent],
    Generic[AnyName, AnyEvent, DistrictName, PartyName],
    total=False,
):
    """Allowed bi-proportional allocator inputs."""

    party_name_f: IPartyNameFunction[AnyName, PartyName]
    """Function to convert names to party names.

    Examples
    --------

    >>> # name for a party at district is (party, district)
    >>> inputs["party_name_f"] = lambda x: x[0]
    """

    district_name_f: IDistrictNameFunction[AnyName, DistrictName]
    """Function to convert names to district names.

    Examples
    --------

    >>> # name for a party at district is (party, district)
    >>> inputs["district_name_f"] = lambda x: x[1]
    """

    candidate_name_f: INameFunction[PartyName, DistrictName, AnyName]
    """Function to get a name from a party name and a district name.

    >>> # name for a party at district is (party, district)
    >>> inputs["candidate_name_f"] = lambda p, d: (p, d)
    """
