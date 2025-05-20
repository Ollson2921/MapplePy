"""Contains the Factor class"""

from typing import Iterable
from itertools import chain
from gridded_cayley_permutations.factors import Factors

from mapplings import MappedTiling, ParameterList, MTCleaner


Cell = tuple[int, int]


class Factor:
    """Class containing algorithms for factoring"""

    def __init__(self, mappling: MappedTiling):
        self.mappling = mappling

    def is_factorable(self) -> bool:
        """Checks if the mappling is factorable"""
        return len(self.find_factor_cells()) > 1

    def find_factor_cells(self) -> tuple[tuple[Cell, ...], ...]:
        """Returns the cells for each factor as a tuple"""
        base_factors = set(
            map(frozenset, Factors(self.mappling.tiling).find_factors_as_cells())
        )
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
        all_regions = set(
            chain(base_factors, avoider_regions, container_regions, enumerator_regions)
        )
        return Factor.combine_cell_groups(list(all_regions))

    def make_factors(
        self, factor_cells: tuple[tuple[Cell, ...], ...]
    ) -> Iterable[MappedTiling]:
        """Creates a new mappling for each factor"""
        for factor in factor_cells:
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

    @staticmethod
    def combine_cell_groups(
        cell_groups: list[frozenset[Cell]],
    ) -> tuple[tuple[Cell, ...], ...]:
        """Joins sets of cells that have a shared intersection"""
        n = len(cell_groups)
        new_cell_groups = cell_groups
        for i in range(n):
            for j in range(n):
                if new_cell_groups[i] & new_cell_groups[j]:
                    combined = new_cell_groups[i] | new_cell_groups[j]
                    new_cell_groups[i] = combined
                    new_cell_groups[j] = combined
        return tuple(map(tuple, set(new_cell_groups)))
