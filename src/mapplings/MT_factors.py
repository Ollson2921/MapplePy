from .mapped_tiling import MappedTiling, Parameter
from tilescope_folder.strategies.factor import Factors
from gridded_cayley_permutations import Tiling


class MTFactor:
    def __init__(self, MappedTiling):
        self.mappling = MappedTiling

    def find_factor_cells(self):
        """Returns a partition of the cells so that the mapped tiling is factored."""
        parameters = self.mappling.all_parameters()
        all_factors = Factors(self.mappling.tiling).find_factors_tracked()
        for parameter in parameters:
            t_factors = all_factors
            p_factors = Factors(parameter.ghost).find_factors_tracked()
            all_factors = []
            queue = t_factors
            while queue:
                t_factor = queue.pop()
                final_t_factor = t_factor
                final_p_factors = []
                new_t_factors = [t_factor]
                while True:
                    new_p_factors = []
                    for t_factor in new_t_factors:
                        p_factors_so_far = self.map_t_factor_to_p_factor(
                            t_factor, parameter, p_factors
                        )
                        p_factors = [p for p in p_factors if p not in p_factors_so_far]
                        for P in p_factors_so_far:
                            final_p_factors += P
                        new_p_factors += p_factors_so_far
                    new_t_factors = []
                    for p_factor in new_p_factors:
                        temp = self.map_p_factor_to_t_factor(p_factor, parameter, queue)
                        new_t_factors += temp
                        queue = [t for t in queue if t not in temp]
                    if not new_t_factors:
                        break
                    for T in new_t_factors:
                        final_t_factor += T
                all_factors.append(final_t_factor)
        return all_factors

    # def is_factorable(self, confidence = 8) -> bool:
    #     """Returns True if no more than 1 factor is nontrivial in regards.
    #     TODO: This is a temporary method and not optimal"""
    #     factor_cells = self.mappling.find_factor_cells()
    #     factors = MappedTiling(self.mappling.tiling, self.mappling.avoiding_parameters,[],[]).make_factors(factor_cells)
    #     non_trivial_factors = 0
    #     for factor in factors:
    #         non_trivial_factors += int(not factor.is_trivial(confidence))
    #         if non_trivial_factors > 1:
    #             return False
    #     return True

    def is_factorable(self, factors):
        non_trivial_factors = 0
        for factor in factors:
            non_trivial_factors += int(not factor.avoiders_are_trivial())
            if non_trivial_factors > 1:
                return False
        return True

    def factor_avoiders(avoiding_parameters, factor, factored_tiling: Tiling):
        """factor is a list of cells for a single factor.
        Returns the factored avoiding parameters
        Skips any parameters which are the same as the factored tiling"""

    def factor_avoiders(self, avoiding_parameters, factor):
        """factor is a list of cells for a single factor.
        Returns the factored avoiding parameters"""
        new_parameters = []
        for avoiding_param in avoiding_parameters:
            new_factor = avoiding_param.sub_parameter(factor)
            if new_factor.ghost == factored_tiling:
                continue
            if new_factor.ghost.active_cells():
                new_parameters.append(new_factor)
        return new_parameters

    def factor_containers(containing_parameters, factor):
        """factor is a list of cells for a single factor.
        Returns 0 if the factor is invalid, otherwise returns the factored containing parameters
        """
        new_parameters = []
        for c_list in containing_parameters:
            new_c_list = []
            for containing_param in c_list:
                new_factor = containing_param.sub_parameter(factor)
                if new_factor.ghost.active_cells():
                    new_c_list.append(new_factor)
            if new_c_list:
                new_parameters.append(new_c_list)
            else:
                return 0
        return new_parameters

    def factor_enumerators(enumeration_parameters, factor):
        """factor is a list of cells for a single factor.
        Returns the factored enumeration parameters"""
        new_parameters = []
        for e_list in enumeration_parameters:
            for enumeration_parameter in e_list:
                new_e_list = []
                new_factor = enumeration_parameter.sub_parameter(factor)
                if new_factor.ghost.active_cells():
                    new_e_list.append(new_factor)
            if new_e_list:
                new_parameters.append(new_e_list)
        return new_parameters

    def make_factors(self, factor_cells):
        for factor in factor_cells:
            factor_containing_parameters = MTFactor.factor_containers(
                self.mappling.containing_parameters, factor
            )
            if type(factor_containing_parameters) is int:
                continue
            factored_tiling = self.mappling.tiling.sub_tiling(factor)
            yield MappedTiling(
                factored_tiling,
                self.factor_avoiders(
                    self.mappling.avoiding_parameters, factor, factored_tiling
                ),
                factor_containing_parameters,
                self.factor_avoiders(self.mappling.enumeration_parameters, factor),
            ).remove_empty_rows_and_columns()

    def find_factors(self):
        return self.make_factors(self.find_factor_cells())

    ####### Interleaving Factors ########
    def find_IL_factor_cells(self):
        """Returns a partition of the cells so that the mapped tiling is factored."""
        parameters = self.mappling.all_parameters()
        all_factors = Factors(self.mappling.tiling).find_IL_factors_tracked()
        for parameter in parameters:
            t_factors = all_factors
            p_factors = Factors(parameter.ghost).find_IL_factors_tracked()
            all_factors = []
            queue = t_factors
            while queue:
                t_factor = queue.pop()
                final_t_factor = t_factor
                final_p_factors = []
                new_t_factors = [t_factor]
                while True:
                    new_p_factors = []
                    for t_factor in new_t_factors:
                        p_factors_so_far = self.map_t_factor_to_p_factor(
                            t_factor, parameter, p_factors
                        )
                        p_factors = [p for p in p_factors if p not in p_factors_so_far]
                        for P in p_factors_so_far:
                            final_p_factors += P
                        new_p_factors += p_factors_so_far
                    new_t_factors = []
                    for p_factor in new_p_factors:
                        temp = self.map_p_factor_to_t_factor(p_factor, parameter, queue)
                        new_t_factors += temp
                        queue = [t for t in queue if t not in temp]
                    if not new_t_factors:
                        break
                    for T in new_t_factors:
                        final_t_factor += T
                all_factors.append(final_t_factor)
        return all_factors

    @staticmethod
    def map_p_factor_to_t_factor(p_factor, parameter, t_factors):
        """maps a factor of the parameter to a list of factors of the tiling"""
        image_cells = set(
            (parameter.map.col_map[cell[0]], parameter.map.row_map[cell[1]])
            for cell in p_factor
        )
        return [
            factor
            for factor in t_factors
            if any(cell in image_cells for cell in factor)
        ]

    @staticmethod
    def map_t_factor_to_p_factor(t_factor, parameter, p_factors):
        """maps a factor of the tiling to a list of parameters"""
        preimage_cells = set()
        for cell in t_factor:
            preimage_cells = preimage_cells.union(parameter.map.preimage_of_cell(cell))
        return [
            factor
            for factor in p_factors
            if any(cell in preimage_cells for cell in factor)
        ]
