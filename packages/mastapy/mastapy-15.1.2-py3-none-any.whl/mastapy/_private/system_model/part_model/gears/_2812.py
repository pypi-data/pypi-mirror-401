"""Gear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private._internal import constructor, utility
from mastapy._private.system_model.part_model import _2738

_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1073
    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import _2715, _2743
    from mastapy._private.system_model.part_model.gears import (
        _2795,
        _2797,
        _2799,
        _2800,
        _2801,
        _2803,
        _2805,
        _2807,
        _2809,
        _2810,
        _2814,
        _2816,
        _2818,
        _2820,
        _2822,
        _2826,
        _2828,
        _2830,
        _2832,
        _2833,
        _2834,
        _2836,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2759

    Self = TypeVar("Self", bound="Gear")
    CastSelf = TypeVar("CastSelf", bound="Gear._Cast_Gear")


__docformat__ = "restructuredtext en"
__all__ = ("Gear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Gear:
    """Special nested class for casting Gear to subclasses."""

    __parent__: "Gear"

    @property
    def mountable_component(self: "CastSelf") -> "_2738.MountableComponent":
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
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2795.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2795

        return self.__parent__._cast(_2795.AGMAGleasonConicalGear)

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
    def concept_gear(self: "CastSelf") -> "_2803.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2803

        return self.__parent__._cast(_2803.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2805.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2805

        return self.__parent__._cast(_2805.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2807.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2807

        return self.__parent__._cast(_2807.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2809.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2809

        return self.__parent__._cast(_2809.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2810.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2810

        return self.__parent__._cast(_2810.FaceGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2816.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2816

        return self.__parent__._cast(_2816.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2818.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2818

        return self.__parent__._cast(_2818.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2820.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2820

        return self.__parent__._cast(_2820.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2822.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2822

        return self.__parent__._cast(_2822.KlingelnbergCycloPalloidSpiralBevelGear)

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
    def worm_gear(self: "CastSelf") -> "_2834.WormGear":
        from mastapy._private.system_model.part_model.gears import _2834

        return self.__parent__._cast(_2834.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2836.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2836

        return self.__parent__._cast(_2836.ZerolBevelGear)

    @property
    def gear(self: "CastSelf") -> "Gear":
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
class Gear(_2738.MountableComponent):
    """Gear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cloned_from(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClonedFrom")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def even_number_of_teeth_required(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EvenNumberOfTeethRequired")

        if temp is None:
            return False

        return temp

    @even_number_of_teeth_required.setter
    @exception_bridge
    @enforce_parameter_types
    def even_number_of_teeth_required(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvenNumberOfTeethRequired",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_clone_gear(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsCloneGear")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def maximum_and_minimum_number_of_teeth_deviation(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAndMinimumNumberOfTeethDeviation"
        )

        if temp is None:
            return None

        return temp

    @maximum_and_minimum_number_of_teeth_deviation.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_and_minimum_number_of_teeth_deviation(
        self: "Self", value: "Optional[int]"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumAndMinimumNumberOfTeethDeviation", value
        )

    @property
    @exception_bridge
    def minimum_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def active_gear_design(self: "Self") -> "_1073.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gear_set(self: "Self") -> "_2814.GearSet":
        """mastapy.system_model.part_model.gears.GearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def shaft(self: "Self") -> "_2759.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def connect_to(self: "Self", other_gear: "Gear") -> None:
        """Method does not return.

        Args:
            other_gear (mastapy.system_model.part_model.gears.Gear)
        """
        pythonnet_method_call(
            self.wrapped, "ConnectTo", other_gear.wrapped if other_gear else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Gear":
        """Cast to another type.

        Returns:
            _Cast_Gear
        """
        return _Cast_Gear(self)
