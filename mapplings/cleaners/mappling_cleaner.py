"""Module with the mapped tiling cleaner"""

from typing import Callable, Iterable
from itertools import chain, product
from functools import partial

from gridded_cayley_permutations import GriddedCayleyPerm, Tiling, RowColMap
from gridded_cayley_permutations.simplify_obstructions_and_requirements import (
    SimplifyObstructionsAndRequirements,
)
from cayley_permutations import CayleyPermutation

from mapplings import MappedTiling, Parameter, ParameterList

from .cleaner import GenericCleaner, Register, CleanerLog
from .parameter_cleaner import ParamCleaner
from .unplacement import ParamUnplacement

default_param_cleaner = ParamCleaner.make_full_cleaner("Param Default Cleaner")


class MTCleaner(GenericCleaner[MappedTiling]):
    """The cleaner for mapped tilings.
    core functions need to be registered with @reg(index)
    where index determines cleaning order"""

    DEBUG = 0
    reg = Register[MappedTiling]()
    global_tracker = CleanerLog[MappedTiling](
        reg.registered_functions, name="Global Tracker"
    )
    all_loggers = {global_tracker}

    # Final Methods
    @staticmethod
    def clean_parameters(
        param_cleaner: ParamCleaner,
    ) -> Callable[[MappedTiling], MappedTiling]:
        """Creates a function (index = 6) that applies a param cleaner to all parameters.
        Must be called to use in list cleanup
        To apply to a mappling, can be run as MTCleaner.make_param_cleaner(param_cleaner)(mappling)
        """

        @MTCleaner.reg(6, update_register=False, log_id="Clean Parameters")
        def _clean_parameters(mappling: MappedTiling) -> MappedTiling:
            temp = mappling.apply_to_all_parameters(
                Parameter.update_active_cells, (mappling.tiling,)
            )
            ParamCleaner.force_log_track(param_cleaner.logger)
            new_avoiders, new_containers, new_enumerators = temp.ace_parameters()
            for func in param_cleaner:
                if getattr(func, "run_on_avoiders"):
                    new_avoiders = ParameterList(
                        param.update_active_cells(mappling.tiling)
                        for param in new_avoiders.apply_to_all(
                            param_cleaner.logger(func)
                        )
                    )
                if getattr(func, "run_on_containers"):
                    new_containers = [
                        ParameterList(
                            param.update_active_cells(mappling.tiling)
                            for param in c_list.apply_to_all(param_cleaner.logger(func))
                        )
                        for c_list in new_containers
                    ]
                if getattr(func, "run_on_containers"):
                    new_enumerators = [
                        ParameterList(
                            param.update_active_cells(mappling.tiling)
                            for param in e_list.apply_to_all(param_cleaner.logger(func))
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
        return MTCleaner.clean_parameters(default_param_cleaner)(mappling)

    @staticmethod
    @reg(7)
    def param_unplacement(mappling: MappedTiling) -> MappedTiling:
        """Applies point unplacement to all avoiders and containers"""
        avoiders, containers, enumerators = mappling.ace_parameters()
        new_avoiders = ParameterList(
            ParamUnplacement(av, mappling).auto_unplace() for av in avoiders
        )
        new_containers = [
            ParameterList(
                ParamUnplacement(co, mappling).auto_unplace() for co in c_list
            )
            for c_list in containers
        ]
        return MappedTiling(mappling.tiling, new_avoiders, new_containers, enumerators)

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
    @reg(9, False)  # Broken
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
    @reg(11, update_register=False)
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
        avoiders: list[Parameter] = []
        for param in new_avoiders:
            if param.dimensions == (0, 0):
                if (
                    not GriddedCayleyPerm(CayleyPermutation(()), ())
                    in param.obstructions
                ):
                    return MappedTiling.empty_mappling()
            else:
                avoiders.append(param)
        new_enumerators: list[ParameterList] = []
        for e_list in mappling.enumerating_parameters:
            new_e_list = e_list.remove_contradictions(base)
            if new_e_list:
                new_enumerators.append(e_list)
        return MappedTiling(mappling.tiling, avoiders, new_containers, new_enumerators)

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
    @reg(13)
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
        avoiders, containers, enumerators = mappling.apply_to_all_parameters(
            param_reducer
        ).ace_parameters()
        new_avoiders = ParameterList(avoiders)
        return MappedTiling(mappling.tiling, new_avoiders, containers, enumerators)

    @staticmethod
    @reg(12)
    def small_ob_inferral(mappling: MappedTiling) -> MappedTiling:
        """Adds point obstructions implied by param point cells
        and small base tiling obstructions"""
        look_for = (
            CayleyPermutation((0, 1)),
            CayleyPermutation((1, 0)),
            CayleyPermutation((0, 0)),
        )
        small_obs = set(ob for ob in mappling.obstructions if ob.pattern in look_for)
        new_mappling = MappedTiling(mappling.tiling, *mappling.ace_parameters())

        for ob in small_obs:
            if ob.pattern == CayleyPermutation((0, 0)):
                new_avoiders = tuple(
                    avoider
                    for avoider in new_mappling.avoiding_parameters.apply_to_all(
                        MTCleaner._cayley_ob_adjust_param, (ob,)
                    )
                )
                new_containers = tuple(
                    ParameterList(
                        c_list.apply_to_all(MTCleaner._cayley_ob_adjust_param, (ob,))
                    )
                    for c_list in new_mappling.containing_parameters
                )
                new_enumerators = tuple(
                    ParameterList(
                        e_list.apply_to_all(MTCleaner._cayley_ob_adjust_param, (ob,))
                    )
                    for e_list in new_mappling.enumerating_parameters
                )
                new_mappling = MappedTiling(
                    new_mappling.tiling, new_avoiders, new_containers, new_enumerators
                )
            else:
                new_avoiders = tuple(
                    avoider
                    for avoider in new_mappling.avoiding_parameters.apply_to_all(
                        MTCleaner._ob_adjust_param, (ob,)
                    )
                )
                new_containers = tuple(
                    ParameterList(
                        c_list.apply_to_all(MTCleaner._ob_adjust_param, (ob,))
                    )
                    for c_list in new_mappling.containing_parameters
                )
                new_enumerators = tuple(
                    ParameterList(
                        e_list.apply_to_all(MTCleaner._ob_adjust_param, (ob,))
                    )
                    for e_list in new_mappling.enumerating_parameters
                )
                new_mappling = MappedTiling(
                    new_mappling.tiling, new_avoiders, new_containers, new_enumerators
                )
        return new_mappling

    @staticmethod
    @reg(8)
    def forward_map_parameter_gcps_from_avoiders(
        mappling: MappedTiling,
    ) -> MappedTiling:
        """Takes gcps with 1-1 map from an avoiding parameter into a tiling"""
        new_base = mappling.tiling
        avoiders, containers, enumerators = mappling.ace_parameters()
        new_avoiders = []
        for avoider in avoiders:
            if not (avoider.obstructions or avoider.requirements):
                new_avoiders.append(avoider)
                continue
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
            new_reqs, add_reqs = [], set[GriddedCayleyPerm]()
            for req_list in avoider.requirements:
                req_list_positions = set(
                    chain.from_iterable((req.positions for req in req_list))
                )
                if not req_list_positions.issubset(injective_cells):
                    new_reqs.append(req_list)
                    continue
                add_reqs.update(set(req_list))
            new_base = new_base.add_obstructions(
                avoider.map.map_gridded_cperms(add_reqs)
            )
            new_obs = {
                ob
                for ob in avoider.obstructions
                if not any((ob.contains_gridded_cperm(req) for req in add_reqs))
            }
            if new_obs or new_reqs:
                new_avoiders.append(
                    Parameter(
                        Tiling(new_obs, new_reqs, avoider.dimensions),
                        avoider.map,
                    )
                )
        return MappedTiling(new_base, new_avoiders, containers, enumerators)

    @staticmethod
    @reg(10)
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
    @reg(14)
    def remove_blank_rows_and_cols_params(mappling: MappedTiling) -> MappedTiling:
        """Deletes all rows and cols in the parameters which have no obs or reqs,
        ignoring point rows and columns and obstructions which are already on the
        base tiling."""
        base_tiling = mappling.tiling
        av_params = []
        for param in mappling.avoiding_parameters:
            av_params.append(param.delete_blank_row_cols_in_param(base_tiling))
        containing_params = []
        for c_list in mappling.containing_parameters:
            new_c_list = []
            for param in c_list:
                new_c_list.append(param.delete_blank_row_cols_in_param(base_tiling))
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
        mappling_point_cells = mappling.point_cells()
        simplify.remove_factors_from_obstructions()
        simplify.remove_redundant_obstructions()
        new_obs = []
        for ob in simplify.obstructions:
            if ob.pattern in (CayleyPermutation([0, 1]), CayleyPermutation([1, 0])):
                if all(
                    position in param.single_value_cells() for position in ob.positions
                ):
                    new_obs.append(ob)
                    continue
            if len(set(ob.positions)) == 1:
                cell = ob.positions[0]
                if (
                    cell in param.single_value_cells()
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
        final_reqs = []
        for req_list in new_reqs:
            new_req_list = [
                req
                for req in req_list
                if all(
                    not param.map.map_gridded_cperm(req).contains_gridded_cperm(ob)
                    for ob in mappling.obstructions
                )
            ]
            if new_req_list:
                final_reqs.append(new_req_list)
            else:
                return Parameter(Tiling.empty_tiling(), RowColMap({}, {}))
        new_ghost = Tiling(new_obs, final_reqs, param.dimensions, simplify=False)
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

    @staticmethod
    def _ob_adjust_param(param: Parameter, input_ob: GriddedCayleyPerm) -> Parameter:

        first_preimages = set(param.map.preimage_of_cell(input_ob.positions[0]))
        second_preimages = set(param.map.preimage_of_cell(input_ob.positions[1]))
        if not (first_preimages and second_preimages):
            return param
        u_cols, u_rows = map(set, zip(*(first_preimages | second_preimages)))
        if len(u_cols) == 1 or len(u_rows) == 1:
            return param
        new_ghost = Tiling(param.obstructions, param.requirements, param.dimensions)
        increasing = input_ob.pattern[0] < input_ob.pattern[1]
        positive_cells = param.positive_cells()
        add_obs = []
        for point in first_preimages & positive_cells:
            for cell in second_preimages:
                if not point[0] < cell[0]:
                    continue
                if (point[1] < cell[1]) == increasing:
                    add_obs.append(GriddedCayleyPerm((0,), [cell]))
        for point in second_preimages & positive_cells:
            for cell in first_preimages:
                if not cell[0] < point[0]:
                    continue
                if (cell[1] < point[1]) == increasing:
                    add_obs.append(GriddedCayleyPerm((0,), [cell]))
        for req_list in param.requirements:
            if all(req.contains(add_obs) for req in req_list):
                return Parameter(Tiling.empty_tiling(), RowColMap({}, {}))
        return Parameter(new_ghost.add_obstructions(add_obs), param.map)

    @staticmethod
    def _cayley_ob_adjust_param(
        param: Parameter, input_ob: GriddedCayleyPerm
    ) -> Parameter:

        point_row_cells = set(product(range(param.dimensions[0]), param.point_rows))
        if not point_row_cells:
            return param
        first_preimages = (
            set(param.map.preimage_of_cell(input_ob.positions[0])) & point_row_cells
        )
        second_preimages = (
            set(param.map.preimage_of_cell(input_ob.positions[1])) & point_row_cells
        )

        if not (first_preimages and second_preimages):
            return param
        u_cols, u_rows = map(set, zip(*(first_preimages | second_preimages)))
        if len(u_cols) == 1 or len(u_rows) == 0:
            return param
        new_ghost = Tiling(param.obstructions, param.requirements, param.dimensions)
        positive_cells = param.positive_cells()
        add_obs = []
        for point in first_preimages & positive_cells:
            for cell in second_preimages:
                if not point[0] < cell[0]:
                    continue
                if point[1] == cell[1]:
                    add_obs.append(GriddedCayleyPerm((0,), [cell]))
        for point in second_preimages & positive_cells:
            for cell in first_preimages:
                if not cell[0] < point[0]:
                    continue
                if cell[1] == point[1]:
                    add_obs.append(GriddedCayleyPerm((0,), [cell]))
        return Parameter(new_ghost.add_obstructions(add_obs), param.map)
