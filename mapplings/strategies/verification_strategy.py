"""Strategies for verifying when a mappling has no parameters,
is horizontal insertion encodable and is vertical insertion
encodable."""

from typing import Optional, Type, TypeVar
from comb_spec_searcher import VerificationStrategy
from gridded_cayley_permutations import GriddedCayleyPerm
from tilescope.strategies import (
    HorizontalInsertionEncodableVerificationStrategy,
    VerticalInsertionEncodableVerificationStrategy,
)

from mapplings import MappedTiling

NoParameterVerificationStrategyT = TypeVar(
    "NoParameterVerificationStrategyT", bound="NoParameterVerificationStrategy"
)

HorizontalInsertionEncodableVerificationStrategyT = TypeVar(
    "HorizontalInsertionEncodableVerificationStrategyT",
    bound="HorizontalInsertionEncodableVerificationStrategy",
)

VerticalInsertionEncodableVerificationStrategyT = TypeVar(
    "VerticalInsertionEncodableVerificationStrategyT",
    bound="VerticalInsertionEncodableVerificationStrategy",
)


class NoParameterVerificationStrategy(
    VerificationStrategy[MappedTiling, GriddedCayleyPerm]
):
    """
    A strategy for verifying if a mappling has no parameters.
    """

    def __init__(
        self,
        rootmt: Optional[MappedTiling] = None,
        ignore_parent: bool = False,
    ):
        self._rootmt: Optional[MappedTiling] = rootmt
        super().__init__(ignore_parent=ignore_parent)

    def change_root(
        self: NoParameterVerificationStrategyT,
        mapped_tiling: MappedTiling,
    ) -> NoParameterVerificationStrategyT:
        """
        Return a new version of the verification strategy with the given mappling instead
        of the current one.
        """
        return self.__class__(mapped_tiling, self.ignore_parent)

    @property
    def rootmt(self) -> Optional[MappedTiling]:
        """The root mapped tiling."""
        return self._rootmt

    def pack(self, comb_class):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from mapplings.strategies.tilescope_strategies import MappedTileScopePack

        return MappedTileScopePack.no_param_ver_point_placement()

    def verified(self, comb_class: MappedTiling) -> bool:
        if (
            comb_class.avoiding_parameters
            or comb_class.containing_parameters
            or comb_class.enumerating_parameters
        ):
            return False
        if comb_class == self.rootmt:
            return False
        return True

    def formal_step(self):
        return "The mappling has no parameters"

    def to_jsonable(self) -> dict:
        d: dict = super().to_jsonable()
        if self._rootmt is not None:
            d["rootmt"] = self._rootmt.to_jsonable()
        return d

    @classmethod
    def from_dict(
        cls: Type[NoParameterVerificationStrategyT], d: dict
    ) -> NoParameterVerificationStrategyT:
        if "rootmt" in d and d["rootmt"] is not None:
            rootmt: Optional[MappedTiling] = MappedTiling.from_dict(d.pop("rootmt"))
        else:
            rootmt = d.pop("rootmt", None)
        return cls(rootmt=rootmt, **d)

    def __repr__(self) -> str:
        args = ", ".join(
            [
                f"root mapped tiling={self._rootmt}",
                f"ignore_parent={self.ignore_parent}",
            ]
        )
        return f"{self.__class__.__name__}({args})"


class MapplingHorizontalInsertionEncodableVerificationStrategy(
    HorizontalInsertionEncodableVerificationStrategy
):
    def verified(self, comb_class: MappedTiling) -> bool:
        return comb_class.tiling.is_horizontal_insertion_encodable()

    def pack(self, comb_class):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from .tilescope_strategies import MappedTileScopePack

        return MappedTileScopePack.horizontal_insertion_encoding()


class MapplingVerticalInsertionEncodableVerificationStrategy(
    VerticalInsertionEncodableVerificationStrategy
):
    def verified(self, comb_class: MappedTiling) -> bool:
        return comb_class.tiling.is_vertical_insertion_encodable()

    def pack(self, comb_class):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from .tilescope_strategies import MappedTileScopePack

        return MappedTileScopePack.vertical_insertion_encoding()