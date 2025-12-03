"""Different strategy packs for MappedTileScope."""

from tilescope.strategies import CellInsertionFactory
from comb_spec_searcher import StrategyPack, AtomStrategy
from mapplings import MappedTiling
from .verification_strategy import (
    NoParameterVerificationStrategy,
    MapplingVerticalInsertionEncodableVerificationStrategy,
    MapplingHorizontalInsertionEncodableVerificationStrategy,
)
from .tilescope_strategies import (
    MapplingPointPlacementFactory,
    MapplingRowPlacementFactory,
    MapplingColPlacementFactory,
    MapplingVerticalInsertionEncodingRequirementInsertionFactory,
    MapplingVerticalInsertionEncodingPlacementFactory,
    MapplingHorizontalInsertionEncodingRequirementInsertionFactory,
    MapplingHorizontalInsertionEncodingPlacementFactory,
    # CleaningStrategy,
    MapplingFactorStrategy,
    MapplingLessThanRowColSeparationStrategy,
    MapplingLessThanOrEqualRowColSeparationStrategy,
)


class MappedTileScopePack(StrategyPack):
    """A strategy pack for mapplings tilescope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def no_param_ver_point_placement(cls):
        """
        Create a point placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
                MapplingPointPlacementFactory(),
            ],
            inferral_strats=[
                # CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    CellInsertionFactory(),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                MapplingVerticalInsertionEncodableVerificationStrategy(),
                MapplingHorizontalInsertionEncodableVerificationStrategy(),
            ],
            name="Point placements, no parameterless verification strategy",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def no_param_ver_row_and_col_placement(cls):
        """
        Create a row and column placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
            ],
            inferral_strats=[
                # CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    MapplingRowPlacementFactory(),
                    MapplingColPlacementFactory(),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                MapplingVerticalInsertionEncodableVerificationStrategy(),
                MapplingHorizontalInsertionEncodableVerificationStrategy(),
            ],
            name="Row and col placements, no parameterless verification strategy",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placement(cls, rootmt: MappedTiling):
        """
        Create a point placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
                MapplingPointPlacementFactory(),
            ],
            inferral_strats=[
                # CleaningStrategy(),  # this is here for tests
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    CellInsertionFactory(),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                NoParameterVerificationStrategy(rootmt),
                MapplingVerticalInsertionEncodableVerificationStrategy(),
                MapplingHorizontalInsertionEncodableVerificationStrategy(),
            ],
            name="Point placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_placement(cls, rootmt: MappedTiling):
        """
        Create a row placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
            ],
            inferral_strats=[
                # CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    MapplingRowPlacementFactory(),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                NoParameterVerificationStrategy(rootmt),
                MapplingVerticalInsertionEncodableVerificationStrategy(),
                MapplingHorizontalInsertionEncodableVerificationStrategy(),
            ],
            name="Row placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def col_placement(cls, rootmt: MappedTiling):
        """
        Create a column placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
            ],
            inferral_strats=[
                # CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    MapplingColPlacementFactory(),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                NoParameterVerificationStrategy(rootmt),
                MapplingVerticalInsertionEncodableVerificationStrategy(),
                MapplingHorizontalInsertionEncodableVerificationStrategy(),
            ],
            name="Column placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_and_col_placement(cls, rootmt: MappedTiling):
        """
        Create a row and column placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
            ],
            inferral_strats=[
                # CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    MapplingRowPlacementFactory(),
                    MapplingColPlacementFactory(),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                NoParameterVerificationStrategy(rootmt),
                MapplingVerticalInsertionEncodableVerificationStrategy(),
                MapplingHorizontalInsertionEncodableVerificationStrategy(),
            ],
            name="Row and col placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_row_and_col_placement(cls, rootmt: MappedTiling):
        """
        Create a point, row and column placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
                MapplingPointPlacementFactory(),
            ],
            inferral_strats=[
                # CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    MapplingRowPlacementFactory(),
                    MapplingColPlacementFactory(),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                NoParameterVerificationStrategy(rootmt),
                MapplingVerticalInsertionEncodableVerificationStrategy(),
                MapplingHorizontalInsertionEncodableVerificationStrategy(),
            ],
            name="Point, row and col placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def vertical_insertion_encoding(cls):
        """
        Create a vertical insertion encoding strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingVerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[],  # Removed Cleaning Strategy
            expansion_strats=[[MapplingVerticalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Vertical Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def horizontal_insertion_encoding(cls):
        """
        Create a horizontal insertion encoding strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingHorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[],  # Removed Cleaning Strategy
            expansion_strats=[[MapplingHorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def insertion_row_and_col_placement(cls, rootmt: MappedTiling):
        """
        Create a row and column placement strategy pack which initially
        makes all cells positive.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
                CellInsertionFactory(),
            ],
            inferral_strats=[
                # CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    MapplingRowPlacementFactory(),
                    MapplingColPlacementFactory(),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                NoParameterVerificationStrategy(rootmt),
                MapplingVerticalInsertionEncodableVerificationStrategy(),
                MapplingHorizontalInsertionEncodableVerificationStrategy(),
            ],
            name="Row and col placements",
            symmetries=[],
            iterative=False,
        )
