from comb_spec_searcher import StrategyPack, AtomStrategy
from .strategies import (
    FactorStrategy,
    ILFactorStrategy,
    MTLessThanRowColSeparationStrategy,
    MTLessThanOrEqualRowColSeparationStrategy,
    MTParamLessThanRowColSeparationStrategy,
    MTParameterPlacementStrategy,
    MTParameterPlacementFactory,
    MTRequirementPlacementStrategy,
    MTPointPlacementFactory,
    MTPartialRequirementPlacementStrategy,
    RowPlacementFactory,
    ColPlacementFactory,
    SpecialInsertionFactory,
    SpecialInsertionStrategy,
    SpecialPatterns,
    MTCellInsertionFactory,
    NoParameterVerificationStrategy,
)


class MappedTileScopePack(StrategyPack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def MTpoint_placement(cls, rootmt):
        return MappedTileScopePack(
            initial_strats=[
                # FactorStrategy(),
                MTPointPlacementFactory(),
                ILFactorStrategy(),
            ],  # Iterable[Strategy]
            inferral_strats=[
                # MTLessThanRowColSeparationStrategy(),
                # MTParamLessThanRowColSeparationStrategy(),
                # MTParameterPlacementFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    MTCellInsertionFactory(),
                    # RowInsertionFactory(),
                    # ColInsertionFactory(),
                    # SpecialInsertionFactory(),
                    # MTLessThanOrEqualRowColSeparationStrategy(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                NoParameterVerificationStrategy(rootmt),
            ],  # Iterable[Strategy]
            name="Point Placement",
            symmetries=[],
            iterative=False,
        )
