"""Contains the Factor class"""

from typing import Iterator
from itertools import chain, combinations
from gridded_cayley_permutations.factors import Factors

from mapplings import MappedTiling, ParameterList, MTCleaner


Cell = tuple[int, int]


class Factor(Factors):
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
            for cell1, cell2 in combinations(region, 2):
                self.combine_cells(cell1, cell2)

    def find_factors_as_cells(self):
        self.combine_cells_from_parameters()
        return super().find_factors_as_cells()

    def temp_find_factors(self) -> Iterator[MappedTiling]:
        """Creates a new mappling for each factor"""
        for factor in self.find_factors_as_cells():
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
            yield MTCleaner.remove_empty_rows_and_cols(new_mappling)
