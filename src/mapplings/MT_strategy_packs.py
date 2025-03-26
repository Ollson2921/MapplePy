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
    RowInsertionFactory,
    ColInsertionFactory,
    SpecialInsertionFactory,
    SpecialInsertionStrategy,
    SpecialPatterns,
)


class MappedTileScopePack(StrategyPack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def MTpoint_placement(cls):
        return MappedTileScopePack(
            initial_strats=[
                FactorStrategy(),
                ILFactorStrategy(),
                MTLessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            inferral_strats=[
                MTLessThanRowColSeparationStrategy(),
                # MTParamLessThanRowColSeparationStrategy(),
                MTParameterPlacementFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    MTPointPlacementFactory(),
                    RowInsertionFactory(),
                    ColInsertionFactory(),
                    SpecialInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[AtomStrategy()],  # Iterable[Strategy]
            name="Point Placement",
            symmetries=[],
            iterative=False,
        )
