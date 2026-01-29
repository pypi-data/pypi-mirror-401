"""ConicalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private.system_model.part_model.gears import _2814

_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1302
    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2704, _2743, _2753
    from mastapy._private.system_model.part_model.gears import (
        _2796,
        _2798,
        _2802,
        _2805,
        _2817,
        _2819,
        _2821,
        _2823,
        _2827,
        _2829,
        _2831,
        _2837,
    )

    Self = TypeVar("Self", bound="ConicalGearSet")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearSet._Cast_ConicalGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSet:
    """Special nested class for casting ConicalGearSet to subclasses."""

    __parent__: "ConicalGearSet"

    @property
    def gear_set(self: "CastSelf") -> "_2814.GearSet":
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
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2796.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2796

        return self.__parent__._cast(_2796.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2798.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2798

        return self.__parent__._cast(_2798.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2802.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2802

        return self.__parent__._cast(_2802.BevelGearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2817.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2817

        return self.__parent__._cast(_2817.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2819.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2819

        return self.__parent__._cast(_2819.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2821.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2821

        return self.__parent__._cast(_2821.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2823.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2823

        return self.__parent__._cast(_2823.KlingelnbergCycloPalloidSpiralBevelGearSet)

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
    def conical_gear_set(self: "CastSelf") -> "ConicalGearSet":
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
class ConicalGearSet(_2814.GearSet):
    """ConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_gear_set_design(self: "Self") -> "_1302.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def conical_gear_set_design(self: "Self") -> "_1302.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def conical_gears(self: "Self") -> "List[_2805.ConicalGear]":
        """List[mastapy.system_model.part_model.gears.ConicalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSet
        """
        return _Cast_ConicalGearSet(self)
