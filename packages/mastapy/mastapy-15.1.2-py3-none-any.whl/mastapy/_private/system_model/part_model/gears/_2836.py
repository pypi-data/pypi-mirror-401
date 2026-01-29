"""ZerolBevelGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

from mastapy._private._internal import constructor, utility
from mastapy._private.system_model.part_model.gears import _2801

_ZEROL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.zerol_bevel import _1078
    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2715, _2738, _2743
    from mastapy._private.system_model.part_model.gears import _2795, _2805, _2812

    Self = TypeVar("Self", bound="ZerolBevelGear")
    CastSelf = TypeVar("CastSelf", bound="ZerolBevelGear._Cast_ZerolBevelGear")


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGear:
    """Special nested class for casting ZerolBevelGear to subclasses."""

    __parent__: "ZerolBevelGear"

    @property
    def bevel_gear(self: "CastSelf") -> "_2801.BevelGear":
        return self.__parent__._cast(_2801.BevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2795.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2795

        return self.__parent__._cast(_2795.AGMAGleasonConicalGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2805.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2805

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
    def zerol_bevel_gear(self: "CastSelf") -> "ZerolBevelGear":
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
class ZerolBevelGear(_2801.BevelGear):
    """ZerolBevelGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bevel_gear_design(self: "Self") -> "_1078.ZerolBevelGearDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def zerol_bevel_gear_design(self: "Self") -> "_1078.ZerolBevelGearDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGear":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGear
        """
        return _Cast_ZerolBevelGear(self)
