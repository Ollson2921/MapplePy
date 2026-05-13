"""Contains the Factor class"""

from itertools import chain, combinations
from functools import cached_property
from gridded_cayley_permutations.factors import Factors
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap

from mapplings import MappedTiling, ParameterList, Parameter
from mapplings.cleaners import MTCleaner

Cell = tuple[int, int]


class MTFactors(Factors):
    """Class containing algorithms for factoring"""

    def __init__(self, mappling: MappedTiling):
        self.mappling = mappling
        super().__init__(mappling.tiling)

    def get_parameter_regions(self) -> set[frozenset[Cell]]:
        """Gets the image regions of all avoiders and all c and e lists."""
        avoider_regions = set(
            frozenset(param.image_cells())
            for param in self.mappling.avoiding_parameters
        )
        container_regions = set(
            frozenset(param_list.combined_image_cells())
            for param_list in self.mappling.containing_parameters
        )
        enumerator_regions = set(
            frozenset(param_list.combined_image_cells())
            for param_list in self.mappling.enumerating_parameters
        )
        return set(chain(avoider_regions, container_regions, enumerator_regions))

    def combine_cells_from_parameters(self) -> None:
        """Uses the parameter regions to combine cells."""
        for region in self.get_parameter_regions():
            region = region & self.mappling.active_cells
            for cell1, cell2 in combinations(region, 2):
                self.combine_cells(cell1, cell2)

    @cached_property
    def find_factors_as_cells(self):
        """Finds the factors as cells."""
        self.combine_cells_from_parameters()
        return super().find_factors_as_cells

    def find_factors(self) -> tuple[MappedTiling, ...]:
        """Creates a new mappling for each factor"""
        all_factors = tuple[MappedTiling, ...]()
        for factor in self.find_factors_as_cells:
            _factor = set(factor)

            new_avoiders = ParameterList(
                avoider
                for avoider in self.mappling.avoiding_parameters
                if avoider.image_cells() & _factor
            )
            new_containers = [
                c_list
                for c_list in self.mappling.containing_parameters
                if c_list.combined_image_cells() & _factor
            ]
            new_enumerators = [
                e_list
                for e_list in self.mappling.enumerating_parameters
                if e_list.combined_image_cells() & _factor
            ]
            new_mappling = MappedTiling(
                self.mappling.tiling.sub_tiling(factor),
                new_avoiders,
                new_containers,
                new_enumerators,
            )
            all_factors += (MTCleaner.remove_empty_rows_and_cols(new_mappling),)
        return all_factors


class MTILFactorNormal(MTFactors):
    """Does IL factoring with 00 obs as normal"""

    @cached_property
    def find_factors_as_cells(self):
        self.combine_cells_in_obs_and_reqs()
        self.combine_cells_from_parameters()
        factors = []
        for val in set(self.cells_dict.values()):
            factor = []
            for cell in self.cells:
                if self.cells_dict[cell] == val:
                    factor.append(cell)
            factors.append(factor)

        return tuple(sorted(tuple(sorted(f)) for f in factors))

    def make_enumerators(self):
        """Creates the enumerators needed for interleaving"""
        factor_rows_and_cols = (
            map(tuple, map(set, zip(*factor))) for factor in self.find_factors_as_cells
        )
        factor_rows_and_cols = tuple(
            map(lambda x: tuple(chain.from_iterable(x)), zip(*factor_rows_and_cols))
        )
        new_enumerators = set()
        dimensions = self.tiling.dimensions
        for row in range(dimensions[1]):
            if factor_rows_and_cols[1].count(row) > 1:
                new_enumerators.add(
                    ParameterList(
                        (
                            Parameter(
                                Tiling([], [], (dimensions[0], 2)),
                                RowColMap(
                                    {i: i for i in range(dimensions[0])},
                                    {0: row, 1: row},
                                ),
                            ),
                        )
                    )
                )
        for col in range(dimensions[0]):
            if factor_rows_and_cols[0].count(col) > 1:
                new_enumerators.add(
                    ParameterList(
                        (
                            Parameter(
                                Tiling([], [], (2, dimensions[1])),
                                RowColMap(
                                    {0: col, 1: col},
                                    {i: i for i in range(dimensions[1])},
                                ),
                            ),
                        )
                    )
                )
        return new_enumerators

    def find_factors(self):
        avoiders, containers, enumerators = self.mappling.ace_parameters()
        self.mappling = MappedTiling(
            self.tiling,
            avoiders,
            containers,
            set(enumerators) | self.make_enumerators(),
        )
        return super().find_factors()


class MTILFactorInverted(MTILFactorNormal):
    """Does IL factoring with the compliment of 00 obs"""

    def combine_cells_in_obs_and_reqs(self):
        new_obs = set()
        for row in range(self.tiling.dimensions[1]):
            for col1, col2 in combinations(range(self.tiling.dimensions[0]), 2):
                new_obs.add(GriddedCayleyPerm((0, 0), ((col1, row), (col2, row))))
        new_obs.symmetric_difference_update(set(self.tiling.obstructions))
        for gcp in new_obs:
            if not self.point_row_ob(gcp):
                for cell, cell2 in combinations((gcp.find_active_cells()), 2):
                    self.combine_cells(cell, cell2)
        for cell, cell2 in chain.from_iterable(
            combinations(
                chain.from_iterable(req.find_active_cells() for req in req_list), 2
            )
            for req_list in self.tiling.requirements
        ):
            self.combine_cells(cell, cell2)
