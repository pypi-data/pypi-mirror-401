"""AGMAGleasonConicalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.part_model.gears import _2805

_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2715, _2738, _2743
    from mastapy._private.system_model.part_model.gears import (
        _2797,
        _2799,
        _2800,
        _2801,
        _2812,
        _2816,
        _2826,
        _2828,
        _2830,
        _2832,
        _2833,
        _2836,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGear")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGear:
    """Special nested class for casting AGMAGleasonConicalGear to subclasses."""

    __parent__: "AGMAGleasonConicalGear"

    @property
    def conical_gear(self: "CastSelf") -> "_2805.ConicalGear":
        return self.__parent__._cast(_2805.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2812.Gear":
        from mastapy._private.system_model.part_model.gears import _2812

        return self.__parent__._cast(_2812.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2738.MountableComponent":
        from mastapy._private.system_model.part_model import _2738

        return self.__parent__._cast(_2738.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2715.Component":
        from mastapy._private.system_model.part_model import _2715

        return self.__parent__._cast(_2715.Component)

    @property
    def part(self: "CastSelf") -> "_2743.Part":
        from mastapy._private.system_model.part_model import _2743

        return self.__parent__._cast(_2743.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2452.DesignEntity":
        from mastapy._private.system_model import _2452

        return self.__parent__._cast(_2452.DesignEntity)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2797.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2797

        return self.__parent__._cast(_2797.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2799.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2799

        return self.__parent__._cast(_2799.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2800.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2800

        return self.__parent__._cast(_2800.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2801.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2801

        return self.__parent__._cast(_2801.BevelGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2816.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2816

        return self.__parent__._cast(_2816.HypoidGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2826.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2826

        return self.__parent__._cast(_2826.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2828.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2828

        return self.__parent__._cast(_2828.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2830.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2830

        return self.__parent__._cast(_2830.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2832.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2832

        return self.__parent__._cast(_2832.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2833.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2833

        return self.__parent__._cast(_2833.StraightBevelSunGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2836.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2836

        return self.__parent__._cast(_2836.ZerolBevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "AGMAGleasonConicalGear":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class AGMAGleasonConicalGear(_2805.ConicalGear):
    """AGMAGleasonConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGear":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGear
        """
        return _Cast_AGMAGleasonConicalGear(self)
