"""MountableComponent"""

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
from mastapy._private.system_model.part_model import _2715

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2452
    from mastapy._private.system_model.connections_and_sockets import (
        _2529,
        _2532,
        _2536,
    )
    from mastapy._private.system_model.part_model import (
        _2705,
        _2709,
        _2716,
        _2718,
        _2734,
        _2735,
        _2740,
        _2743,
        _2745,
        _2747,
        _2748,
        _2754,
        _2756,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2863,
        _2866,
        _2869,
        _2872,
        _2874,
        _2876,
        _2883,
        _2885,
        _2892,
        _2895,
        _2896,
        _2897,
        _2899,
        _2901,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2853
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
        _2812,
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

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2715.Component":
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
    def bearing(self: "CastSelf") -> "_2709.Bearing":
        from mastapy._private.system_model.part_model import _2709

        return self.__parent__._cast(_2709.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2718.Connector":
        from mastapy._private.system_model.part_model import _2718

        return self.__parent__._cast(_2718.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2734.MassDisc":
        from mastapy._private.system_model.part_model import _2734

        return self.__parent__._cast(_2734.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2735.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2735

        return self.__parent__._cast(_2735.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2740.OilSeal":
        from mastapy._private.system_model.part_model import _2740

        return self.__parent__._cast(_2740.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2745.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2745

        return self.__parent__._cast(_2745.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2747.PointLoad":
        from mastapy._private.system_model.part_model import _2747

        return self.__parent__._cast(_2747.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2748.PowerLoad":
        from mastapy._private.system_model.part_model import _2748

        return self.__parent__._cast(_2748.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2754.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2754

        return self.__parent__._cast(_2754.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2756.VirtualComponent":
        from mastapy._private.system_model.part_model import _2756

        return self.__parent__._cast(_2756.VirtualComponent)

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
    def gear(self: "CastSelf") -> "_2812.Gear":
        from mastapy._private.system_model.part_model.gears import _2812

        return self.__parent__._cast(_2812.Gear)

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
    def ring_pins(self: "CastSelf") -> "_2853.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2853

        return self.__parent__._cast(_2853.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2863.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2863

        return self.__parent__._cast(_2863.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2866.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2866

        return self.__parent__._cast(_2866.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2869.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2869

        return self.__parent__._cast(_2869.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2872.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2872

        return self.__parent__._cast(_2872.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2874.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2874

        return self.__parent__._cast(_2874.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2876.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2876

        return self.__parent__._cast(_2876.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2883.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2883

        return self.__parent__._cast(_2883.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2885.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2885

        return self.__parent__._cast(_2885.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2892.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2892

        return self.__parent__._cast(_2892.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2895.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2895

        return self.__parent__._cast(_2895.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2896.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2896

        return self.__parent__._cast(_2896.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2897.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2897

        return self.__parent__._cast(_2897.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2899.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2899

        return self.__parent__._cast(_2899.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2901.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2901

        return self.__parent__._cast(_2901.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2715.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def inner_component(self: "Self") -> "_2705.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_connection(self: "Self") -> "_2532.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_socket(self: "Self") -> "_2536.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @exception_bridge
    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2705.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2529.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2705.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2716.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)
