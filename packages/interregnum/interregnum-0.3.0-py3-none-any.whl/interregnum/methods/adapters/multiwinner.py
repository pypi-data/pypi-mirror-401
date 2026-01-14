# SPDX-FileCopyrightText: 2025 wmj <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# #!/usr/bin/env python
"""Adapters to convert single-winner methods to multi-winner methods."""
from __future__ import annotations
from typing import (
    Callable,
    TypeVar,
    Iterable,
    Generic,
    Any,
    cast,
    Concatenate,
)
import dataclasses as dt
from typing_extensions import override

from ...exceptions import PreconditionError
from ...types import Score
from ..types import (
    check_seats,
    NonDeterministicAllocator,
    NonDeterministicState,
    NonDeterministicResult,
    Candidate,
    Input,
    CandidateFilter,
    AnyName,
)
from ..events import (
    EventLog,
    TieEvent,
    QuotaWinnerEvent,
    IneligibleEvent,
)

from ...random import RandomSeed
from .ranking import (
    Ranking,
    RankingList,
    break_tie_ranking,
)


@dt.dataclass
class MultiWinnerResultData(EventLog):
    """Multi-winner result data."""

    threshold: Score = 0
    remaining_seats: int = 0
    rounds: int = 0


MultiDataT = TypeVar("MultiDataT", bound=MultiWinnerResultData)


@dt.dataclass
class MultiWinnerState(NonDeterministicState, Generic[MultiDataT, AnyName]):
    """A calculation state from multi-winner-adapter."""

    data: MultiDataT

    def break_tie(
        self, candidates: Iterable[Candidate[AnyName]], ascending: bool
    ) -> dict[str, list[Candidate[AnyName]]]:
        """Break ties based on a ranking list, or choose randomly if not possible."""
        return break_tie_ranking(
            RankingList(candidates, ascending),
            limit=self.data.remaining_seats,
            fallback=self.random_tie_break,
        )


DataT = TypeVar("DataT")
IDataT = TypeVar("IDataT")


# get winners from a ranking function
class MultiWinnerAdapter(
    NonDeterministicAllocator[AnyName, MultiDataT], Generic[AnyName, MultiDataT, DataT, IDataT]
):
    """Create a multi-winner allocator from a single-winner allocator.

    Given N seats, this method will give each seat for the most ranked candidate
    in succesive rounds,
    """

    def __init__(
        self,
        make_input_f: Callable[Concatenate[IDataT, ...], DataT],
        ranking_f: Callable[..., Ranking[AnyName]],
        required_input: Input,
        optional_input: Input,
    ):
        """Create a multi-winner adapter.

        Args
        ----
        make_input_f
            input data formatter
        ranking_f
            a ranking method
        required_input
            declaration of required inputs for the calc method
        optional_input
            declaration of optional inputs for the calc method
        """
        super().__init__(required_input, optional_input)
        self._make_input_f = make_input_f
        self._ranking_f = ranking_f

    def _init_data(self) -> MultiWinnerResultData:
        return MultiWinnerResultData()

    def _reset(self, random_seed: RandomSeed | None) -> MultiWinnerState[MultiDataT, AnyName]:
        return MultiWinnerState(random_seed=random_seed, data=cast(MultiDataT, self._init_data()))

    def _base_ranking_kwargs(self) -> dict[str, Any]:
        return {}

    def _build_input(self, data: IDataT, **ranking_args: Any) -> DataT:
        return self._make_input_f(data, **ranking_args)

    def _build_ranking(
        self, state: MultiWinnerState[MultiDataT, AnyName], candidates: DataT, **ranking_args: Any
    ) -> Ranking[AnyName]:
        ranking_args.update(self._base_ranking_kwargs())
        return self._ranking_f(candidates, **ranking_args)

    def _build_result(
        self, state: MultiWinnerState[MultiDataT, AnyName], elected: list[Candidate[AnyName]]
    ) -> NonDeterministicResult[AnyName, MultiDataT]:
        return state.make_result(elected, state.data)

    def _check_precondition(self, score: Ranking[AnyName]) -> None:
        pass

    def _calc(
        self,
        data: IDataT,
        seats: int,
        random_seed: RandomSeed | None = None,
        filter_f: CandidateFilter[AnyName, Any] | None = None,
        **ranking_args: Any,
    ) -> tuple[MultiWinnerState[MultiDataT, AnyName], NonDeterministicResult[AnyName, MultiDataT]]:
        check_seats(seats)
        state: MultiWinnerState[MultiDataT, AnyName] = self._reset(random_seed)

        state.data.remaining_seats = seats
        elected = []

        scores = self._build_ranking(state, self._build_input(data), **ranking_args)
        if filter_f:
            for name in filter_f.exclusion_list():
                scores.remove_name(name)
                state.data.log.append(IneligibleEvent(target=name, criterion="initial_exclusion"))

        self._check_precondition(scores)

        state.data.rounds = 0
        while state.data.remaining_seats and not scores.empty():
            # get scores
            winners = scores.winners()
            state.data.threshold = winners[0].votes

            if len(winners) > state.data.remaining_seats:
                # tie
                state.data.log.append(
                    TieEvent(
                        candidates=tuple(elem.name for elem in winners),
                        condition={"best_score": state.data.threshold},
                    )
                )
                # log
                batches = state.break_tie(winners, scores.ascending())
            else:
                batches = {"best_score": winners}

            for criterion, items in batches.items():
                for cand in items:
                    elected.append(cand.with_seats(1))
                    state.data.log.append(
                        QuotaWinnerEvent(
                            target=cand.name, quota=state.data.threshold, criterion=criterion
                        )
                    )
                    state.data.remaining_seats -= 1
                    if state.data.remaining_seats:
                        scores.remove(cand)
                    if filter_f:
                        state.data.log.extend(filter_f.update(elected[-1]))

            if filter_f:
                for name in filter_f.exclusion_list():
                    scores.remove_name(name)

            state.data.rounds += 1

        return state, self._build_result(state, elected)


# winner-takes-all form a ranking function
class WinnerTakesAllAdapter(MultiWinnerAdapter[AnyName, MultiDataT, DataT, IDataT]):
    """Winner Takes All Adapter using a ranking list."""

    def __init__(
        self,
        make_input_f: Callable[Concatenate[IDataT, ...], DataT],
        ranking_f: Callable[..., Ranking[AnyName]],
        required_input: Input,
        optional_input: Input,
    ):
        """Create a Winner Takes All adapter.

        Args
        ----
        make_input_f
            input data formatter
        ranking_f
            a ranking method
        required_input
            declaration of required inputs for the calc method
        optional_input
            declaration of optional inputs for the calc method
        """
        super().__init__(
            make_input_f,
            ranking_f=ranking_f,
            required_input=required_input,
            optional_input=optional_input,
        )

    def _call_calc(
        self, data: IDataT, **kwargs: Any
    ) -> tuple[MultiWinnerState[MultiDataT, AnyName], NonDeterministicResult[AnyName, MultiDataT]]:
        return super()._calc(data, **kwargs)

    @override
    def _calc(
        self,
        data: IDataT,
        seats: int = 1,
        random_seed: RandomSeed | None = None,
        filter_f: CandidateFilter[AnyName, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[MultiWinnerState[MultiDataT, AnyName], NonDeterministicResult[AnyName, MultiDataT]]:
        if filter_f:
            if seats > 1:
                raise PreconditionError("filter_f is not supported")
            kwargs["filter_f"] = filter_f
        check_seats(seats)
        state, result = self._call_calc(data, seats=1, random_seed=random_seed, **kwargs)
        if seats == 1:
            return state, result
        elected = [x.with_seats(seats) for x in result.allocation]
        assert result.data
        return state, state.make_result(elected, result.data)
