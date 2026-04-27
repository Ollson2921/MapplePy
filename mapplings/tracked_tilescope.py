"""
A tracked searcher adapted from Tilings for use with GriddedCayleyPermutations.

Original: https://github.com/PermutaTriangle/Tilings/blob/develop/tilings/tilescope.py
"""

from typing import Iterator, Optional
from collections import Counter, deque
from comb_spec_searcher import CombinatorialSpecificationSearcher, StrategyPack
from comb_spec_searcher.typing import CSSstrategy, CombinatorialClassType, WorkPacket
from comb_spec_searcher.strategies.rule import AbstractRule
from comb_spec_searcher.class_queue import DefaultQueue, CSSQueue
import tabulate
from mapplings import MappedTiling


class TrackedSearcher(CombinatorialSpecificationSearcher):
    """
    A TileScope that will prioritise expanding tilings whose underlying tilings
    were found at earlier levels. It does this by keeping a queue for each level,
    and adding tilings to the queue that the underlying was first found at.

    The first time a queue changes level, the next level of queue i will be added
    to the curr level of queue i + 1. If `delay_next` is False then it continues
    in this way for future change levels but if it is False (the default) the next
    level of queue i will be added to the curr level of queue i after the first
    change levels.
    """

    def __init__(
        self,
        start_class: MappedTiling,
        strategy_pack: StrategyPack,
        max_cvs: Optional[int] = None,
        delay_next: bool = False,
        **kwargs,
    ) -> None:
        self.max_cvs = max_cvs
        super().__init__(
            start_class,
            strategy_pack,
            classqueue=TrackedQueue(strategy_pack, self, delay_next),
            **kwargs,
        )

    def _rules_from_strategy(  # type: ignore
        self, comb_class: CombinatorialClassType, strategy: CSSstrategy
    ) -> Iterator[AbstractRule]:
        """
        Yield all the rules given by a strategy/strategy factory whose children all
        satisfy the max_assumptions constraint.
        """

        # pylint: disable=arguments-differ
        def num_cvs(child: MappedTiling) -> int:
            return len(child.extra_parameters)

        for rule in super()._rules_from_strategy(comb_class, strategy):
            if self.max_cvs is None or all(
                num_cvs(child) <= self.max_cvs for child in rule.children
            ):
                yield rule


class TrackedDefaultQueue(DefaultQueue):
    """A deafult queue for tracked tilings."""

    def __init__(self, pack: StrategyPack, delay_next: bool):
        super().__init__(pack)
        self.next_curr_level: Optional[tuple[deque[int], ...]] = None
        self.delay_next = delay_next

    def is_empty(self) -> bool:
        """Return whether the queue is empty."""
        return bool(
            not self.working and not self.next_level and not any(self.curr_level)
        )

    def set_next_curr_level(self, other: "TrackedDefaultQueue"):
        """Set the next current level for this default queue."""
        self.next_curr_level = other.curr_level

    def set_tracked_queue(self, tracked_queue: "TrackedQueue") -> None:
        """Set the tracked queue for this default queue."""
        self._inferral_expanded = tracked_queue.inferral_expanded
        self._initial_expanded = tracked_queue.initial_expanded
        self.ignore = tracked_queue.ignore

    def _change_level(self) -> None:
        assert not self.staging, "Can't change level is staging is not empty"
        assert not self.working, "Can't change level is working is not empty"
        assert not any(self.curr_level), "Can't change level is curr_level is not empty"
        assert self.next_curr_level is not None, "not set the next curr queue"
        if any(self.next_curr_level):
            # this ensures we only change level when the next curr queue is empty
            # and therefore makes sure we never expand a label with the same strategy
            # twice
            raise StopIteration
        self.next_curr_level[0].extend(
            label
            for label, _ in sorted(self.next_level.items(), key=lambda x: -x[1])
            if label not in self.ignore
        )
        self.next_level: Counter[int] = Counter()
        if not self.delay_next:
            self.next_curr_level = self.curr_level
        if not any(self.curr_level):
            raise StopIteration


class TrackedQueue(CSSQueue):
    """A queue for tracked tilings."""

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self, pack: StrategyPack, tilescope: TrackedSearcher, delay_next: bool
    ):
        """A queue of labels"""
        # pylint: disable=too-many-instance-attributes
        self.tilescope = tilescope
        self.pack = pack
        self.delay_next = delay_next
        self.label_to_underlying: dict[int, int] = {}
        self._level_first_found: dict[int, int] = {}
        self._underlyng_labels_per_level: Counter[int] = Counter()
        self._all_labels_per_level: Counter[int] = Counter()
        self.inferral_expanded: set[int] = set()
        self.initial_expanded: set[int] = set()
        self.ignore: set[int] = set()
        first_queue = TrackedDefaultQueue(pack, self.delay_next)
        first_queue.set_tracked_queue(self)
        self.queues = [first_queue]
        self.add_new_queue()

        super().__init__(pack)

    @property
    def levels_completed(self):
        """Return the number of levels completed for underlying tilings"""
        return len(self.queues) - 2

    def add_new_queue(self) -> None:
        """Add a new queue for the next level of underlying tilings."""
        last_queue = self.queues[-1]
        new_queue = TrackedDefaultQueue(self.pack, self.delay_next)
        new_queue.set_tracked_queue(self)
        last_queue.set_next_curr_level(new_queue)
        self.queues.append(new_queue)

    def get_underlying_label(self, label: int) -> int:
        """Return the underlying label for a given label."""
        underlying_label = self.label_to_underlying.get(label)
        if underlying_label is None:
            tiling = self.tilescope.classdb.get_class(label)
            underlying_tiling = tiling.remove_enumerators()
            underlying_label = self.tilescope.classdb.get_label(underlying_tiling)
            self.label_to_underlying[label] = underlying_label
            # count the number of labels that will be added to this level
            self._all_labels_per_level[self.level_first_found(underlying_label)] += 1
        return underlying_label

    def level_first_found(self, label: int) -> int:
        """Return the level that the underlying label was first found at."""
        underlying_label = self.get_underlying_label(label)
        level = self._level_first_found.get(underlying_label)
        if level is None:
            level = len(self.queues) - 2
            self._level_first_found[underlying_label] = level
            # count the number of underlying labels added to this level
            self._underlyng_labels_per_level[level] += 1
        return level

    def add(self, label: int) -> None:
        if label in self.ignore:
            return
        self.queues[self.level_first_found(label)].add(label)

    def set_not_inferrable(self, label: int) -> None:
        self.queues[self.level_first_found(label)].set_not_inferrable(label)

    def set_verified(self, label: int) -> None:
        self.queues[self.level_first_found(label)].set_verified(label)

    def set_stop_yielding(self, label: int) -> None:
        self.queues[self.level_first_found(label)].set_stop_yielding(label)

    def do_level(self) -> Iterator[WorkPacket]:
        raise NotImplementedError

    def status(self) -> str:
        status = f"Queue status (currently on level {self.levels_completed}):\n"
        table: list[tuple[str, ...]] = []
        working = ("working",) + tuple(
            f"{len(queue.working):,d}" for queue in self.queues[:-1]
        )
        table.append(working)
        for idx in range(len(self.pack.expansion_strats)):
            current = (f"current (set {idx + 1})",) + tuple(
                f"{len(queue.curr_level[idx]):,d}" for queue in self.queues[:-1]
            )
            table.append(current)
        nxt = ("next",) + tuple(
            f"{len(queue.next_level):,d}" for queue in self.queues[:-1]
        )
        table.append(nxt)
        status += "    "
        headers = ("Size",) + tuple(
            f"Queue {idx}" for idx in range(len(self.queues) - 1)
        )
        underlying = ("underlying",) + tuple(
            str(self._underlyng_labels_per_level[level])
            for level in range(len(self.queues))
        )
        table.append(underlying)
        all_labels = ("all labels",) + tuple(
            str(self._all_labels_per_level[level]) for level in range(len(self.queues))
        )
        table.append(all_labels)
        table = [headers] + table
        table = list(zip(*table))
        headers = table[0]
        table = table[1:]
        colalign = ("left",) + tuple("right" for _ in headers[1:])
        status += (
            tabulate.tabulate(table, headers=headers, colalign=colalign).replace(
                "\n", "\n    "
            )
            + "\n"
        )
        return status

    def __next__(self) -> WorkPacket:
        for idx, queue in enumerate(self.queues):
            if idx == len(self.queues) - 1:
                if all(queue.is_empty() for queue in self.queues):
                    raise StopIteration
                self.add_new_queue()
            try:
                return next(queue)
            except StopIteration:
                continue
        raise StopIteration("No elements in queue")
