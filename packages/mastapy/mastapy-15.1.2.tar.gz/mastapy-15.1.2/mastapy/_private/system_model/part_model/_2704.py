"""AbstractAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

from mastapy._private._internal import conversion, utility
from mastapy._private.system_model.part_model import _2743

_ABSTRACT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.part_model import (
        _2703,
        _2713,
        _2715,
        _2726,
        _2737,
        _2751,
        _2753,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2860,
        _2862,
        _2865,
        _2868,
        _2871,
        _2873,
        _2884,
        _2891,
        _2893,
        _2898,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2851
    from mastapy._private.system_model.part_model.gears import (
        _2796,
        _2798,
        _2802,
        _2804,
        _2806,
        _2808,
        _2811,
        _2814,
        _2817,
        _2819,
        _2821,
        _2823,
        _2824,
        _2827,
        _2829,
        _2831,
        _2835,
        _2837,
    )

    Self = TypeVar("Self", bound="AbstractAssembly")
    CastSelf = TypeVar("CastSelf", bound="AbstractAssembly._Cast_AbstractAssembly")


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssembly:
    """Special nested class for casting AbstractAssembly to subclasses."""

    __parent__: "AbstractAssembly"

    @property
    def part(self: "CastSelf") -> "_2743.Part":
        return self.__parent__._cast(_2743.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2452.DesignEntity":
        from mastapy._private.system_model import _2452

        return self.__parent__._cast(_2452.DesignEntity)

    @property
    def assembly(self: "CastSelf") -> "_2703.Assembly":
        from mastapy._private.system_model.part_model import _2703

        return self.__parent__._cast(_2703.Assembly)

    @property
    def bolted_joint(self: "CastSelf") -> "_2713.BoltedJoint":
        from mastapy._private.system_model.part_model import _2713

        return self.__parent__._cast(_2713.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2726.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2726

        return self.__parent__._cast(_2726.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2737.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2737

        return self.__parent__._cast(_2737.MicrophoneArray)

    @property
    def root_assembly(self: "CastSelf") -> "_2751.RootAssembly":
        from mastapy._private.system_model.part_model import _2751

        return self.__parent__._cast(_2751.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2753.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2753

        return self.__parent__._cast(_2753.SpecialisedAssembly)

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
    def concept_gear_set(self: "CastSelf") -> "_2804.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2804

        return self.__parent__._cast(_2804.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2806.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2806

        return self.__parent__._cast(_2806.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2808.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2808

        return self.__parent__._cast(_2808.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2811.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2811

        return self.__parent__._cast(_2811.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2814.GearSet":
        from mastapy._private.system_model.part_model.gears import _2814

        return self.__parent__._cast(_2814.GearSet)

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
    def planetary_gear_set(self: "CastSelf") -> "_2824.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2824

        return self.__parent__._cast(_2824.PlanetaryGearSet)

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
    def worm_gear_set(self: "CastSelf") -> "_2835.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2835

        return self.__parent__._cast(_2835.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2837.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2837

        return self.__parent__._cast(_2837.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2851.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2851

        return self.__parent__._cast(_2851.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2860.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2860

        return self.__parent__._cast(_2860.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2862.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2862

        return self.__parent__._cast(_2862.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2865.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2865

        return self.__parent__._cast(_2865.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2868.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2868

        return self.__parent__._cast(_2868.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2871.CVT":
        from mastapy._private.system_model.part_model.couplings import _2871

        return self.__parent__._cast(_2871.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2873.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2873

        return self.__parent__._cast(_2873.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2884.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2884

        return self.__parent__._cast(_2884.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2891.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2891

        return self.__parent__._cast(_2891.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2893.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2893

        return self.__parent__._cast(_2893.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2898.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2898

        return self.__parent__._cast(_2898.TorqueConverter)

    @property
    def abstract_assembly(self: "CastSelf") -> "AbstractAssembly":
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
class AbstractAssembly(_2743.Part):
    """AbstractAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mass_of_assembly(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfAssembly")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def components_with_unknown_mass_properties(
        self: "Self",
    ) -> "List[_2715.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ComponentsWithUnknownMassProperties"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def components_with_zero_mass_properties(self: "Self") -> "List[_2715.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentsWithZeroMassProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssembly":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssembly
        """
        return _Cast_AbstractAssembly(self)
