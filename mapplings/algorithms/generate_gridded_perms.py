from functools import cache, cached_property
from typing import TYPE_CHECKING, Iterator, NamedTuple, Optional, Tuple, Dict
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm, RowColMap
from gridded_cayley_permutations.minimal_gridded_cperms import MinimalGriddedCayleyPerm
from collections import namedtuple, Counter
from heapq import heapify, heappop, heappush
from itertools import chain, product


GPTuple = Tuple[GriddedCayleyPerm, ...]
Requirements = Tuple[GPTuple, ...]
PreimagesTuple = Tuple[GPTuple, ...]
ContainingPreimages = Tuple[PreimagesTuple, ...]
ACEPreimages = Tuple[PreimagesTuple, ContainingPreimages, ContainingPreimages]

Cell = Tuple[int, int]
if TYPE_CHECKING:
    from mapplings import MappedTiling
    from mapplings.parameter import Parameter
    from mapplings.parameter_list import ParameterList


class QueuePacket(NamedTuple):
    gp: GriddedCayleyPerm
    preimages: ACEPreimages  # is a valid preimage or can be extended to one
    last_cell: Cell
    mindices: dict[Cell, int]
    satisfies_reqs: bool

    def __lt__(self, other: "QueuePacket"):
        return self.gp < other.gp


class GriddedCayleyPerms:
    """
    Yield the GriddedCayleyPermutation on the underlying tiling of a mappling,
    together with the preimages on each of the parameters.
    """

    def __init__(self, mappling: "MappedTiling"):
        self._mappling = mappling
        self._underlying = mappling.tiling
        self.obstructions = self._underlying.obstructions
        self.requirements = self._underlying.requirements
        self.active_cells = self._mappling.active_cells
        self.avoiding_parameters = self._mappling.avoiding_parameters
        self.containing_parameters = self._mappling.containing_parameters
        self.enumerating_parameters = self._mappling.enumerating_parameters
        self.queue: list[QueuePacket] = []
        self.yielded_so_far: set["GriddedCayleyPerm"] = set()

    def initialise_queue(self) -> None:
        heapify(self.queue)
        preimages = (
            tuple((GriddedCayleyPerm([], []),) for _ in self.avoiding_parameters),
            tuple(
                tuple((GriddedCayleyPerm([], []),) for _ in co)
                for co in self.containing_parameters
            ),
            tuple(
                tuple((GriddedCayleyPerm([], []),) for _ in en)
                for en in self.enumerating_parameters
            ),
        )
        qpacket = QueuePacket(
            GriddedCayleyPerm([], []),
            preimages,
            (-1, -1),
            {},
            not (bool(self.requirements)),
        )
        heappush(self.queue, qpacket)

    def gridded_cayley_perms(
        self, max_size: int
    ) -> Iterator[Tuple[GriddedCayleyPerm, ACEPreimages]]:
        if self._mappling.tiling.is_empty():
            return
        self.initialise_queue()
        while self.queue:
            qpacket = heappop(self.queue)
            yield from self.try_yield(qpacket)
            for new_qpacket in self.extend_by_one_point(qpacket):
                if len(new_qpacket.gp) <= max_size:
                    self.try_push(new_qpacket)

    def try_push(self, qpacket: QueuePacket) -> None:
        if self.satisfies_requirements(
            qpacket.gp, self.requirements_up_to_cell(qpacket.last_cell)
        ) and all(any(True for _ in co) for co in qpacket.preimages[1]):
            heappush(self.queue, qpacket)

    def try_yield(
        self, qpacket: QueuePacket
    ) -> Iterator[Tuple[GriddedCayleyPerm, ACEPreimages]]:
        if self.satisfies_requirements(qpacket.gp):
            ace_preimages = self.valid_ace_preimages(qpacket.preimages)
            if self.satisfies_parameters(ace_preimages, valid=True) and all(
                any(x for x in co) for co in qpacket.preimages[1]  # can be satisfied
            ):
                yield qpacket.gp, ace_preimages

    def valid_preimage(self, preimage: GPTuple, parameter: "Parameter"):
        return tuple(
            gp
            for gp in preimage
            if self.satisfies_obstructions_and_requirements(
                gp, parameter.obstructions, parameter.requirements
            )
        )

    def valid_ace_preimages(self, ace_preimages: ACEPreimages):
        avoiding = tuple(
            self.valid_preimage(av_preimage, av_param)
            for av_preimage, av_param in zip(ace_preimages[0], self.avoiding_parameters)
        )
        containing = tuple(
            tuple(
                self.valid_preimage(preimage, param)
                for preimage, param in zip(preimages, param_list)
            )
            for preimages, param_list in zip(
                ace_preimages[1], self.containing_parameters
            )
        )

        enumerating = tuple(
            tuple(
                self.valid_preimage(preimage, param)
                for preimage, param in zip(preimages, param_list)
            )
            for preimages, param_list in zip(
                ace_preimages[2], self.enumerating_parameters
            )
        )
        return avoiding, containing, enumerating

    def satisfies_parameters(self, ace_preimages: ACEPreimages, valid=False):
        if valid:
            avoiding, containing, _ = ace_preimages
        else:
            avoiding, containing, _ = self.valid_ace_preimages(ace_preimages)
        # check every avoiding tuple is empty
        # and every containing tuple is non-empty
        return not any(x for x in avoiding) and all(
            any(x for x in co) for co in containing
        )

    def satisfies_obstructions(
        self, gp: GriddedCayleyPerm, obstructions: Optional[GPTuple] = None
    ):
        if obstructions is None:
            obstructions = self.obstructions
        return gp.avoids(obstructions)

    def satisfies_requirements(
        self, gp: GriddedCayleyPerm, requirements: Optional[Requirements] = None
    ):
        if requirements is None:
            requirements = self.requirements
        return all(gp.contains(req) for req in requirements)

    def satisfies_obstructions_and_requirements(
        self,
        gp: GriddedCayleyPerm,
        obstructions: Optional[GPTuple] = None,
        requirements: Optional[Requirements] = None,
    ):
        return self.satisfies_obstructions(
            gp, obstructions
        ) and self.satisfies_requirements(gp, requirements)

    @cache
    def requirements_up_to_cell(self, cell: Cell) -> Requirements:
        return tuple(
            tuple(
                gp.sub_gridded_cayley_perm(set(c for c in gp.positions if c < cell))
                for gp in req_list
            )
            for req_list in self.requirements
        )

    def extend_by_one_point(self, qpacket: QueuePacket) -> Iterator[QueuePacket]:
        """Extends the gridded cayley perm by one point."""
        for cell in self.cells_to_try(qpacket):
            for index, next_gp, ace_preimages in self.insert_point(qpacket, cell):
                satisfies_reqs = qpacket.satisfies_reqs or self.satisfies_requirements(
                    next_gp
                )
                if self.satisfies_obstructions(next_gp) and self.satisfies_parameters(
                    ace_preimages
                ):
                    new_mindices = {
                        c: i if i <= index else i + 1
                        for c, i in qpacket.mindices.items()
                        if c != cell
                    }
                    new_mindices[cell] = index + 1
                    if satisfies_reqs and not qpacket.satisfies_reqs:
                        yield QueuePacket(
                            next_gp,
                            ace_preimages,
                            (-1, -1),
                            new_mindices,
                            satisfies_reqs,
                        )
                    else:
                        yield QueuePacket(
                            next_gp, ace_preimages, cell, new_mindices, satisfies_reqs
                        )

    def cells_to_try(self, qpacket: QueuePacket) -> Iterator[Cell]:
        """
        Return the cells to try for the nex point.
        The bool tells us if we still need to insert
        points to satisfy the requirements
        """
        if not qpacket.satisfies_reqs:
            cell_counts = Counter(qpacket.gp.positions)
            filled_cells = [
                cell
                for cell in cell_counts
                if cell_counts[cell] >= self.max_cell_counts
            ]
            restriced_reqs = tuple(
                tuple(gp.get_gridded_perm_in_cells(filled_cells) for gp in req)
                for req in self.requirements
            )
            if not self.satisfies_requirements(qpacket.gp, restriced_reqs):
                return
            for cell, count in sorted(self.max_cell_counts.items()):
                if count > cell_counts[cell]:
                    yield cell
        else:
            for cell in self.active_cells:
                if cell >= qpacket.last_cell:
                    yield cell

    @cached_property
    def max_cell_counts(self):
        max_cell_counts = Counter()
        for gps in self.requirements:
            counts, cells = [], set()
            for gp in gps:
                counts.append(Counter(gp.positions))
                cells.update(gp.positions)
            max_per_req = Counter(
                {cell: max(count[cell] for count in counts) for cell in cells}
            )
            max_cell_counts.update(max_per_req)
        return max_cell_counts

    def insert_point(
        self, qpacket: QueuePacket, cell
    ) -> Iterator[Tuple[int, GriddedCayleyPerm, ACEPreimages]]:
        mindex, maxdex, minval, maxval = qpacket.gp.bounding_box_of_cell(cell)
        mindex = max(mindex, qpacket.mindices.get(cell, 0))
        for index in range(maxdex, mindex - 1, -1):
            for val in range(minval, maxval + 1):
                for new_gcp, new_preimages in self.insert_specific_point(
                    qpacket, cell, index, val
                ):
                    # this check needs to take into account subgp in image region
                    # for gp in chain(
                    #     *new_preimages[0],
                    #     *[p for pl in new_preimages[1] for p in pl],
                    #     *[p for pl in new_preimages[2] for p in pl],
                    # ):
                    #     assert new_gcp.pattern.contains_pattern(
                    #         gp.pattern
                    #     ), f"{new_gcp}, {gp}"
                    yield index, new_gcp, new_preimages

    def insert_specific_point(
        self, qpacket: QueuePacket, cell: Cell, index: int, value: int
    ) -> Iterator[tuple[GriddedCayleyPerm, ACEPreimages]]:
        gp = qpacket.gp
        new_positions = gp.positions[:index] + (cell,) + gp.positions[index:]
        if value in gp.values_in_row(cell[1]):
            new_pattern = CayleyPermutation(
                gp.pattern[:index] + (value,) + gp.pattern[index:]
            )
            preimages = self.insert_specific_point_in_ace_preimages(
                qpacket, cell, index, value, repeat=True
            )
            yield GriddedCayleyPerm(new_pattern, new_positions), preimages
        updated_pattern = tuple(val if val < value else val + 1 for val in gp.pattern)
        new_pattern = CayleyPermutation(
            updated_pattern[:index] + (value,) + updated_pattern[index:]
        )
        preimages = self.insert_specific_point_in_ace_preimages(
            qpacket, cell, index, value, repeat=False
        )
        yield GriddedCayleyPerm(new_pattern, new_positions), preimages

    def insert_specific_point_in_ace_preimages(
        self,
        qpacket: QueuePacket,
        cell: Cell,
        index: int,
        value: int,
        repeat: bool,
    ) -> ACEPreimages:
        av, co, en = qpacket.preimages

        def update_preimages(preimages: GPTuple, parameter: "Parameter"):
            if cell in parameter.image_cells():
                pre_index = sum(
                    1
                    for i, cell in enumerate(qpacket.gp.positions)
                    if i < index and cell in parameter.image_cells()
                )
                pre_values = set(
                    qpacket.gp.pattern[i]
                    for i, cell in enumerate(qpacket.gp.positions)
                    if qpacket.gp.pattern[i] <= value
                    and cell in parameter.image_cells()
                )
                pre_value = len(pre_values)
                if value in pre_values:
                    pre_value -= 1
                if repeat and value in pre_values:
                    return tuple(
                        chain.from_iterable(
                            self.insert_specific_point_in_preimage(
                                gp, parameter, cell, pre_index, pre_value, repeat=True
                            )
                            for gp in preimages
                        )
                    )
                return tuple(
                    chain.from_iterable(
                        self.insert_specific_point_in_preimage(
                            gp, parameter, cell, pre_index, pre_value, repeat=False
                        )
                        for gp in preimages
                    )
                )
            return preimages

        new_av = tuple(
            update_preimages(preimages, parameter)
            for preimages, parameter in zip(av, self.avoiding_parameters)
        )
        new_co = tuple(
            tuple(
                update_preimages(preimages, parameter)
                for preimages, parameter in zip(co_list, param_list)
            )
            for co_list, param_list in zip(co, self.containing_parameters)
        )
        new_en = tuple(
            tuple(
                update_preimages(preimages, parameter)
                for preimages, parameter in zip(en_list, param_list)
            )
            for en_list, param_list in zip(en, self.enumerating_parameters)
        )
        return new_av, new_co, new_en

    def insert_specific_point_in_preimage(
        self,
        preimage: GriddedCayleyPerm,
        parameter: "Parameter",
        cell: Cell,
        index: int,
        value: int,
        repeat: bool,
    ) -> Iterator[GriddedCayleyPerm]:
        col, row = cell
        left_index = (
            preimage.positions[index - 1][0] if 0 <= (index - 1) < len(preimage) else 0
        )
        right_index = (
            preimage.positions[index][0]
            if index < len(preimage)
            else parameter.dimensions[0]
        )
        cols = [
            c
            for c in parameter.map.preimages_of_col(col)
            if left_index <= c <= right_index
        ]

        value_to_row = {
            v: preimage.positions[i][1] for i, v in enumerate(preimage.pattern)
        }
        if repeat:
            low_value = value_to_row[value]
            high_value = value_to_row[value]
        else:
            lower_rows = [r for v, r in value_to_row.items() if v < value]
            higher_rows = [r for v, r in value_to_row.items() if v >= value]
            low_value = max(lower_rows) if lower_rows else 0
            high_value = min(higher_rows) if higher_rows else parameter.dimensions[1]
        rows = [
            r
            for r in parameter.map.preimages_of_row(row)
            if low_value <= r <= high_value
        ]
        for insert_cell in product(cols, rows):
            new_positions = (
                preimage.positions[:index] + (insert_cell,) + preimage.positions[index:]
            )
            if repeat:
                new_pattern = CayleyPermutation(
                    preimage.pattern[:index] + (value,) + preimage.pattern[index:]
                )
                new_preimage = GriddedCayleyPerm(new_pattern, new_positions)
            else:
                updated_pattern = tuple(
                    val if val < value else val + 1 for val in preimage.pattern
                )
                new_pattern = CayleyPermutation(
                    updated_pattern[:index] + (value,) + updated_pattern[index:]
                )
                new_preimage = GriddedCayleyPerm(new_pattern, new_positions)
            if self.satisfies_obstructions(new_preimage, parameter.obstructions):
                yield new_preimage


if __name__ == "__main__":
    from gridded_cayley_permutations import Tiling
    from mapplings import MappedTiling, Parameter, ParameterList

    mappling = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
            ),
            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
            (3, 3),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (2, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((2, 0, 1)),
                                        ((1, 0), (2, 0), (3, 0)),
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((2, 0, 1)),
                                        ((1, 0), (2, 0), (4, 0)),
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((2, 0, 1)),
                                        ((1, 1), (2, 1), (3, 1)),
                                    ),
                                ),
                            ),
                            (5, 2),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 0, 3: 0, 4: 2}, {0: 0, 1: 2}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 0), (3, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1, 2)),
                                        ((0, 0), (2, 0), (3, 0)),
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1, 2)),
                                        ((1, 0), (2, 0), (3, 0)),
                                    ),
                                ),
                            ),
                            (5, 1),
                        ),
                        RowColMap({0: 0, 1: 2, 2: 2, 3: 2, 4: 2}, {0: 0}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1, 2)),
                                        ((0, 0), (1, 0), (2, 0)),
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1, 2)),
                                        ((0, 0), (1, 0), (2, 1)),
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1, 2)),
                                        ((0, 0), (1, 1), (2, 1)),
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1, 2)),
                                        ((0, 1), (1, 1), (2, 1)),
                                    ),
                                ),
                            ),
                            (4, 2),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 2}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (1, 0))
                                    ),
                                ),
                            ),
                            (2, 1),
                        ),
                        RowColMap({0: 2, 1: 2}, {0: 0}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (2, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((2, 0, 1)),
                                        ((1, 0), (2, 0), (3, 0)),
                                    ),
                                ),
                            ),
                            (4, 1),
                        ),
                        RowColMap({0: 2, 1: 2, 2: 2, 3: 2}, {0: 0}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (1, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                    ),
                                ),
                            ),
                            (2, 2),
                        ),
                        RowColMap({0: 0, 1: 0}, {0: 0, 1: 2}),
                    ),
                }
            )
        ),
        (
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                    ),
                                ),
                                (),
                                (2, 2),
                            ),
                            RowColMap({0: 0, 1: 2}, {0: 0, 1: 2}),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                    ),
                                ),
                                (),
                                (2, 2),
                            ),
                            RowColMap({0: 0, 1: 2}, {0: 0, 1: 2}),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                    ),
                                ),
                                (),
                                (3, 2),
                            ),
                            RowColMap({0: 0, 1: 2, 2: 2}, {0: 0, 1: 2}),
                        ),
                    }
                )
            ),
        ),
        (),
    )

    N = 3
    print(mappling)
    for gcp in sorted(mappling.get_objects(N)[tuple()]):
        print(gcp)
    GCP = GriddedCayleyPerms(mappling)
    for gcp, preimages in sorted(GCP.gridded_cayley_perms(max_size=N)):
        if len(gcp) == N:
            print(gcp, preimages)

    # assert 0

    from gridded_cayley_permutations import Tiling
    from mapplings.parameter import Parameter
    from mapplings.parameter_list import ParameterList
    from mapplings import MappedTiling

    ghost = Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)]),
            GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 0)]),
        ],
        [],
        (2, 1),
    )

    containing_params = (
        ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0})),)),
    )
    mappling = MappedTiling(
        Tiling(
            [],
            [],
            (1, 1),
        ),
        [],
        containing_params,
        [],
    )

    p1 = Parameter.make_vincular((0, 1, 2), (2,))
    p2 = Parameter.make_vincular((2, 0, 1), (1,))

    base = Tiling([GriddedCayleyPerm((2, 1, 0), ((0, 0), (0, 0), (0, 0)))], [], (1, 1))
    base = Tiling([GriddedCayleyPerm((0, 0), ((0, 0), (0, 0)))], [], (1, 1))
    mappling = MappedTiling(base, [p1, p2], containing_params, [])

    from mapplings.strategies.mapped_tilescope import MappedTileScopePack
    from comb_spec_searcher import CombinatorialSpecificationSearcher

    searcher = CombinatorialSpecificationSearcher(
        mappling, MappedTileScopePack.point_row_and_col_placement(mappling)
    )
    searcher.do_level()
    searcher.do_level()
    searcher.do_level()
    # searcher.do_level()
    N = 4
    old, new = 0, 0
    for mappling in searcher.classdb.comb_class_list:

        GCP = GriddedCayleyPerms(mappling)
        import time

        print("CURRENT")
        terms = []
        for i in range(N + 1):
            start = time.time()
            terms.append(len(mappling.get_objects(i)[tuple()]))
            print(
                i,
                terms[-1],
                round(time.time() - start, 2),
                "seconds",
            )
            old += time.time() - start

        print("NEW")
        c = -1
        count = 0
        start = time.time()
        new_terms = [0 for _ in range(N + 1)]
        for gp, preimages in GCP.gridded_cayley_perms(max_size=N):
            if len(gp) > c:
                if c >= 0:
                    new_terms[len(gp) - 1] = count
                    print(len(gp) - 1, count, round(time.time() - start, 2), "seconds")
                count = 0
                c = len(gp)
                new += time.time() - start
                start = time.time()
            count += 1
        new_terms[len(gp)] = count
        print(len(gp), count, round(time.time() - start, 2), "seconds")
        new += time.time() - start
        assert all(
            x == y for x, y in zip(new_terms, terms)
        ), f"Error with:\n{mappling}\nOld: {terms}\nNew: {new_terms}\nRepr:\n{repr(mappling)}"
        # print("=" * 10)
        # print(gp)
        # assert mappling.gcp_satisfies_containing_params(gp)
        # for preimage in preimages:
        #     print("\t", preimage)
        print("OLD", round(old, 2), "seconds")
        print("NEW", round(new, 2), "seconds")
