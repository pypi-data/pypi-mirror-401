"""BevelGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.part_model.gears import _2796

_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2704, _2743, _2753
    from mastapy._private.system_model.part_model.gears import (
        _2798,
        _2806,
        _2814,
        _2827,
        _2829,
        _2831,
        _2837,
    )

    Self = TypeVar("Self", bound="BevelGearSet")
    CastSelf = TypeVar("CastSelf", bound="BevelGearSet._Cast_BevelGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSet:
    """Special nested class for casting BevelGearSet to subclasses."""

    __parent__: "BevelGearSet"

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2796.AGMAGleasonConicalGearSet":
        return self.__parent__._cast(_2796.AGMAGleasonConicalGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2806.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2806

        return self.__parent__._cast(_2806.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2814.GearSet":
        from mastapy._private.system_model.part_model.gears import _2814

        return self.__parent__._cast(_2814.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2753.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2753

        return self.__parent__._cast(_2753.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2704.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2704

        return self.__parent__._cast(_2704.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2743.Part":
        from mastapy._private.system_model.part_model import _2743

        return self.__parent__._cast(_2743.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2452.DesignEntity":
        from mastapy._private.system_model import _2452

        return self.__parent__._cast(_2452.DesignEntity)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2798.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2798

        return self.__parent__._cast(_2798.BevelDifferentialGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2827.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2827

        return self.__parent__._cast(_2827.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2829.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2829

        return self.__parent__._cast(_2829.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2831.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2831

        return self.__parent__._cast(_2831.StraightBevelGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2837.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2837

        return self.__parent__._cast(_2837.ZerolBevelGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "BevelGearSet":
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
class BevelGearSet(_2796.AGMAGleasonConicalGearSet):
    """BevelGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearSet":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSet
        """
        return _Cast_BevelGearSet(self)
