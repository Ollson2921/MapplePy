"""Module with the mapped tiling cleaner"""

from typing import Callable, Iterable
from itertools import chain, product
from functools import partial

from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from gridded_cayley_permutations.simplify_obstructions_and_requirements import (
    SimplifyObstructionsAndRequirements,
)
from cayley_permutations import CayleyPermutation

from mapplings import MappedTiling, Parameter, ParameterList

from .cleaner import GenericCleaner, Register
from .parameter_cleaner import ParamCleaner


class MTCleaner(GenericCleaner[MappedTiling]):
    """The cleaner for mapped tilings.
    core functions need to be registered with @reg(index)
    where index determines cleaning order"""

    DEBUG = 0
    reg = Register[MappedTiling]("mappling_register")

    # Final Methods
    @staticmethod
    def clean_parameters(
        param_cleaner: ParamCleaner,
    ) -> Callable[[MappedTiling], MappedTiling]:
        """Creates a function (index = 6) that applies a param cleaner to all parameters.
        Must be called to use in list cleanup
        To apply to a mappling, can be run as MTCleaner.make_param_cleaner(param_cleaner)(mappling)
        """

        @MTCleaner.reg(6, update_register=False)
        def _clean_parameters(mappling: MappedTiling) -> MappedTiling:
            temp = mappling.apply_to_all_parameters(
                Parameter.update_active_cells, (mappling.tiling,)
            )
            new_avoiders, new_containers, new_enumerators = temp.ace_parameters()
            for func in param_cleaner:
                if getattr(func, "run_on_avoiders"):
                    new_avoiders = ParameterList(
                        param.update_active_cells(mappling.tiling)
                        for param in new_avoiders.apply_to_all(func)
                    )
                if getattr(func, "run_on_containers"):
                    new_containers = [
                        ParameterList(
                            param.update_active_cells(mappling.tiling)
                            for param in c_list.apply_to_all(func)
                        )
                        for c_list in new_containers
                    ]
                if getattr(func, "run_on_containers"):
                    new_enumerators = [
                        ParameterList(
                            param.update_active_cells(mappling.tiling)
                            for param in e_list.apply_to_all(func)
                        )
                        for e_list in new_enumerators
                    ]
            return MappedTiling(
                mappling.tiling, new_avoiders, new_containers, new_enumerators
            )

        return _clean_parameters

    @staticmethod
    @reg(6)
    def fully_clean_parameters(mappling: MappedTiling) -> MappedTiling:
        """Applies all parameter cleanning functions to all parameters"""
        return MTCleaner.clean_parameters(ParamCleaner.make_full_cleaner())(mappling)

    @staticmethod
    @reg(0)
    def try_to_kill(mappling: MappedTiling) -> MappedTiling:
        """Used to decide how to kill mapplings in full_cleanup"""
        if mappling.is_empty():
            return MappedTiling.empty_mappling()
        if not mappling.tiling.active_cells:
            if any(
                not avoider.ghost.active_cells
                for avoider in mappling.avoiding_parameters
            ):
                return MappedTiling.empty_mappling()
            return MappedTiling(
                Tiling(
                    [GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),))], [], (1, 1)
                ),
                [],
                [],
                [],
            )
        return mappling

    @staticmethod
    @reg(8, False)  # Broken
    def factor_containters(mappling: MappedTiling) -> MappedTiling:
        """Factors out the intersection factors of a containing parameter list"""
        new_containers = list(
            chain(
                *(
                    MTCleaner._find_intersection(c_list)
                    for c_list in mappling.containing_parameters
                )
            )
        )
        new_mappling = MappedTiling(
            mappling.tiling,
            mappling.avoiding_parameters,
            new_containers,
            mappling.enumerating_parameters,
        )
        return MTCleaner.list_cleanup(
            new_mappling,
            (MTCleaner.reap_all_contradictions, MTCleaner.reduce_all_parameter_gcps),
        )

    @staticmethod
    @reg(10, update_register=False)
    def backmap_points(mappling: MappedTiling) -> MappedTiling:
        """Backmaps point obstructions to all parameters"""
        point_obstructions = (ob for ob in mappling.obstructions if len(ob) == 1)
        return mappling.apply_to_all_parameters(
            Parameter.backmap_obstructions, (point_obstructions,)
        )

    @staticmethod
    @reg(1)
    def reap_all_contradictions(mappling: MappedTiling) -> MappedTiling:
        """Removes any contradictory parameters
        and kills the mappling if all containers in a c-list are contradictory"""
        base = mappling.tiling
        new_containers = []
        for c_list in mappling.containing_parameters:
            if not c_list:
                continue
            new_c_list = c_list.remove_contradictions(base)
            if not new_c_list:
                return MappedTiling.empty_mappling()
            new_containers.append(new_c_list)
        new_avoiders = mappling.avoiding_parameters.remove_contradictions(base)
        new_enumerators = []
        for e_list in mappling.enumerating_parameters:
            new_e_list = e_list.remove_contradictions(base)
            if new_e_list:
                new_enumerators.append(e_list)
        return MappedTiling(
            mappling.tiling, new_avoiders, new_containers, new_enumerators
        )

    @staticmethod
    @reg(2)
    def reap_contradictions_from_positive_cells(mappling: MappedTiling) -> MappedTiling:
        """Removes parameters if there is a contradiction coming from the ghost's positive cells"""
        new_avoiders = ParameterList(
            avoider
            for avoider in mappling.avoiding_parameters
            if avoider.positive_cells_are_valid(mappling)
        )
        new_containers = []
        for container_list in mappling.containing_parameters:
            new_c_list = ParameterList(
                container
                for container in container_list
                if container.positive_cells_are_valid(mappling)
            )
            if not new_c_list:
                return MappedTiling.empty_mappling()
            new_containers.append(new_c_list)
        return MappedTiling(
            mappling.tiling,
            new_avoiders,
            new_containers,
            mappling.enumerating_parameters,
        )

    @staticmethod
    @reg(3)
    def remove_empty_rows_and_cols(mappling: MappedTiling) -> MappedTiling:
        """Removes empty rows and cols in the base tiling and removes
        preimage rows and cols from the parameters"""
        if mappling == MappedTiling.empty_mappling():
            return mappling
        empty_cols, empty_rows = mappling.find_empty_rows_and_columns()
        if (
            len(empty_cols) == mappling.dimensions[0]
            or len(empty_rows) == mappling.dimensions[1]
        ):
            if any(param.requirements for param in mappling.avoiding_parameters) or any(
                all(param.requirements for param in param_list)
                for param_list in mappling.containing_parameters
            ):
                return MappedTiling.empty_mappling()
            return MappedTiling(
                Tiling(
                    [GriddedCayleyPerm(CayleyPermutation((0,)), [(0, 0)])], [], (1, 1)
                ),
                ParameterList([]),
                [],
                [],
            )
        new_tiling = mappling.delete_rows_and_columns(empty_cols, empty_rows)
        new_mappling = MappedTiling(
            new_tiling,
            mappling.avoiding_parameters,
            mappling.containing_parameters,
            mappling.enumerating_parameters,
        )
        return new_mappling.apply_to_all_parameters(
            Parameter.delete_preimage_of_rows_and_columns, (empty_cols, empty_rows)
        )

    @staticmethod
    @reg(12)
    def simple_reduce_redundant_parameters(mappling: MappedTiling) -> MappedTiling:
        """Removes any parameter implied by another with a basic check"""
        new_avoiders = mappling.avoiding_parameters.simple_remove_redundant()
        new_containers = [
            c_list.simple_remove_redundant()
            for c_list in mappling.containing_parameters
        ]
        return MappedTiling(
            mappling.tiling,
            new_avoiders,
            new_containers,
            mappling.enumerating_parameters,
        )

    @staticmethod
    @reg(4)
    def reduce_all_parameter_gcps(mappling: MappedTiling) -> MappedTiling:
        """Removes all obs and reqs that are implied by the base tiling from all Parameters"""
        param_reducer = partial(MTCleaner._reduce_parameter_gcps, mappling)
        return mappling.apply_to_all_parameters(param_reducer)

    @staticmethod
    @reg(11)
    def small_ob_inferral(mappling: MappedTiling) -> MappedTiling:
        """Adds point obstructions implied by param point cells
        and small base tiling obstructions"""
        look_for = (CayleyPermutation((0, 1)), CayleyPermutation((1, 0)))
        small_obs = set(ob for ob in mappling.obstructions if ob.pattern in look_for)
        new_mappling = MappedTiling(mappling.tiling, *mappling.ace_parameters())

        def adjust_param(param: Parameter, input_ob: GriddedCayleyPerm) -> Parameter:
            new_ghost = Tiling(param.obstructions, param.requirements, param.dimensions)
            increasing = input_ob.pattern[0] < input_ob.pattern[1]
            point_cells = param.point_cells()
            first_preimages = set(param.map.preimage_of_cell(input_ob.positions[0]))
            second_preimages = set(param.map.preimage_of_cell(input_ob.positions[1]))
            add_obs = []
            for point in first_preimages & point_cells:
                for cell in second_preimages:
                    if not point[0] < cell[0]:
                        continue
                    if (point[1] < cell[1]) == increasing:
                        add_obs.append(GriddedCayleyPerm((0,), [cell]))
            for point in second_preimages & point_cells:
                for cell in first_preimages:
                    if not cell[0] < point[0]:
                        continue
                    if (cell[1] < point[1]) == increasing:
                        add_obs.append(GriddedCayleyPerm((0,), [cell]))
            return Parameter(new_ghost.add_obstructions(add_obs), param.map)

        for ob in small_obs:
            new_mappling = new_mappling.apply_to_all_parameters(adjust_param, (ob,))
        return new_mappling

    @staticmethod
    @reg(7)
    def forward_map_parameter_gcps_from_avoiders(
        mappling: MappedTiling,
    ) -> MappedTiling:
        """Takes gcps with 1-1 map from an avoiding parameter into a tiling"""
        new_base = mappling.tiling
        avoiders, containers, enumerators = mappling.ace_parameters()
        new_avoiders = []
        for avoider in avoiders:
            empty_cells = (
                set(product(range(avoider.dimensions[0]), range(avoider.dimensions[1])))
                - avoider.active_cells
            )
            injective_cells = avoider.active_cells & (
                avoider.injective_cells() - avoider.point_cells()
            )
            if injective_cells == avoider.active_cells and empty_cells:
                new_avoiders.append(avoider)
                continue
            new_reqs = []
            for req_list in avoider.requirements:
                req_list_positions = set(
                    chain.from_iterable((req.positions for req in req_list))
                )
                if not req_list_positions.issubset(injective_cells):
                    new_reqs.append(req_list)
                    continue
                new_base = new_base.add_obstructions(
                    avoider.map.map_gridded_cperms(req_list)
                )
            new_obs = avoider.obstructions
            if new_obs or new_reqs:
                new_avoiders.append(
                    Parameter(
                        Tiling(new_obs, new_reqs, avoider.dimensions),
                        avoider.map,
                    )
                )
        return MappedTiling(new_base, new_avoiders, containers, enumerators)

    @staticmethod
    @reg(9)
    def forward_map_parameter_gcps_from_containers(
        mappling: MappedTiling,
    ) -> MappedTiling:
        """Takes gcps with 1-1 map from a containing parameter into a tiling"""
        new_base = mappling.tiling
        avoiders, containers, enumerators = mappling.ace_parameters()
        new_containers = []
        for c_list in containers:
            if len(c_list) > 1:
                new_containers.append(c_list)
                continue
            container = list(c_list)[0]
            injective_cells = container.injective_cells()
            new_obs, add_obs = (
                tuple[GriddedCayleyPerm, ...](),
                tuple[GriddedCayleyPerm, ...](),
            )
            for ob in container.obstructions:
                if not set(ob.positions).issubset(injective_cells):
                    new_obs += (ob,)
                    continue
                add_obs += (ob,)
            new_base = new_base.add_obstructions(
                container.map.map_gridded_cperms(add_obs)
            )
            new_reqs = []
            for req_list in container.requirements:
                if not set(
                    chain.from_iterable((req.positions for req in req_list))
                ).issubset(injective_cells):
                    new_reqs.append(req_list)
                    continue
                new_base = new_base.add_requirement_list(
                    container.map.map_gridded_cperms(req_list)
                )
            if new_obs or new_reqs:
                new_containers.append(
                    ParameterList(
                        (
                            Parameter(
                                Tiling(new_obs, new_reqs, container.dimensions),
                                container.map,
                            ),
                        )
                    )
                )
        return MappedTiling(new_base, avoiders, new_containers, enumerators)

    @staticmethod
    @reg(5)
    def reap_blank(mappling: MappedTiling) -> MappedTiling:
        """Kills mappling if any avoiders are blank,
        and removes any c_lists with blank containers"""
        for param in mappling.avoiding_parameters:
            if not param.not_blank_cells():
                return MappedTiling.empty_mappling()
        new_containeres = []
        for c_list in mappling.containing_parameters:
            if any(not (param.not_blank_cells()) for param in c_list):
                continue
            new_containeres.append(c_list)
        return MappedTiling(
            mappling.tiling,
            mappling.avoiding_parameters,
            new_containeres,
            mappling.enumerating_parameters,
        )

    @staticmethod
    @reg(13)
    def remove_blank_rows_and_cols_params(mappling: MappedTiling) -> MappedTiling:
        """Deletes all rows and cols in the parameters which have no obs or reqs,
        ignoring point rows and columns and obstructions which are already on the
        base tiling."""
        base_tiling = mappling.tiling
        av_params = []
        for param in mappling.avoiding_parameters:
            blank_cols, blank_rows = param.find_blank_columns_and_rows_in_param(
                base_tiling
            )
            cols_to_remove = set()
            rows_to_remove = set()
            for i in range(param.dimensions[0] - 1):
                if i in blank_cols and i + 1 in blank_cols:
                    cols_to_remove.add(i + 1)
            for j in range(param.dimensions[1] - 1):
                if j in blank_rows and j + 1 in blank_rows:
                    rows_to_remove.add(j + 1)
            av_params.append(
                param.delete_rows_and_columns(cols_to_remove, rows_to_remove)
            )
        containing_params = []
        for c_list in mappling.containing_parameters:
            new_c_list = []
            for param in c_list:
                blank_cols, blank_rows = param.find_blank_columns_and_rows_in_param(
                    base_tiling
                )
                cols_to_remove = set()
                rows_to_remove = set()
                for i in range(param.dimensions[0] - 1):
                    if i in blank_cols and i + 1 in blank_cols:
                        cols_to_remove.add(i + 1)
                for j in range(param.dimensions[1] - 1):
                    if j in blank_rows and j + 1 in blank_rows:
                        rows_to_remove.add(j + 1)
                new_c_list.append(
                    param.delete_rows_and_columns(cols_to_remove, rows_to_remove)
                )
            containing_params.append(ParameterList(new_c_list))
        return MappedTiling(
            mappling.tiling,
            ParameterList(av_params),
            containing_params,
            mappling.enumerating_parameters,
        )

    # Internal Methods

    @staticmethod
    def _insert_param(tiling: Tiling, param: Parameter) -> Tiling:
        return tiling.add_obstructions(
            param.map.map_gridded_cperms(param.obstructions)
        ).add_requirements(param.map.map_requirements(param.requirements))

    @staticmethod
    def _reduce_parameter_gcps(mappling: MappedTiling, param: Parameter) -> Parameter:
        """Removes all obs and reqs from param that are implied by mappling"""
        simplify = SimplifyObstructionsAndRequirements(
            param.obstructions,
            param.map.preimage_of_requirements(mappling.requirements),
            mappling.dimensions,
        )
        point_cells = param.point_cells()
        mappling_point_cells = mappling.point_cells()
        simplify.remove_factors_from_obstructions()
        simplify.remove_redundant_obstructions()
        new_obs = []
        for ob in simplify.obstructions:
            if len(set(ob.positions)) == 1:
                cell = ob.positions[0]
                if (
                    cell in point_cells
                    and (param.col_map[cell[0]], param.row_map[cell[1]])
                    not in mappling_point_cells
                ):
                    new_obs.append(ob)
                    continue
            if any(
                param.map.map_gridded_cperm(ob).contains_gridded_cperm(mt_ob)
                for mt_ob in mappling.obstructions
            ):
                continue
            new_obs.append(ob)
        new_reqs = [
            req_list
            for req_list in param.requirements
            if not simplify.requirement_implied_by_some_requirement(
                req_list, simplify.requirements
            )
        ]
        new_ghost = Tiling(new_obs, new_reqs, param.dimensions, simplify=False)
        return Parameter(new_ghost, param.map)

    @staticmethod
    def _find_intersection(container_list: ParameterList) -> Iterable[ParameterList]:
        """Returns the intersection of the factors of the container list"""
        if len(container_list) == 1:
            return [
                ParameterList([factor]) for factor in tuple(container_list)[0].factor()
            ]
        all_factors = tuple(map(set, container_list.apply_to_all(Parameter.factor)))
        intersection = all_factors[0]
        for factors in all_factors:
            intersection = intersection & factors
            if not intersection:
                return [
                    container_list,
                ]
        image_cells = set(chain(*(factor.image_cells() for factor in intersection)))
        new_param_list = ParameterList([])
        for param in container_list:
            keep_cells = param.map.preimage_of_cells(param.image_cells() - image_cells)
            new_param_list.add(param.sub_parameter(keep_cells))
        return [new_param_list] + [ParameterList([factor]) for factor in intersection]
