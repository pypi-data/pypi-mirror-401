"""Part"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.implicit import overridable
from mastapy._private.system_model import _2452

_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility import _1731
    from mastapy._private.system_model.connections_and_sockets import _2532
    from mastapy._private.system_model.import_export import _2502
    from mastapy._private.system_model.part_model import (
        _2703,
        _2704,
        _2705,
        _2706,
        _2709,
        _2712,
        _2713,
        _2715,
        _2718,
        _2719,
        _2724,
        _2725,
        _2726,
        _2727,
        _2734,
        _2735,
        _2736,
        _2737,
        _2738,
        _2740,
        _2745,
        _2747,
        _2748,
        _2751,
        _2753,
        _2754,
        _2756,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2860,
        _2862,
        _2863,
        _2865,
        _2866,
        _2868,
        _2869,
        _2871,
        _2872,
        _2873,
        _2874,
        _2876,
        _2883,
        _2884,
        _2885,
        _2891,
        _2892,
        _2893,
        _2895,
        _2896,
        _2897,
        _2898,
        _2899,
        _2901,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2851, _2852, _2853
    from mastapy._private.system_model.part_model.gears import (
        _2795,
        _2796,
        _2797,
        _2798,
        _2799,
        _2800,
        _2801,
        _2802,
        _2803,
        _2804,
        _2805,
        _2806,
        _2807,
        _2808,
        _2809,
        _2810,
        _2811,
        _2812,
        _2814,
        _2816,
        _2817,
        _2818,
        _2819,
        _2820,
        _2821,
        _2822,
        _2823,
        _2824,
        _2826,
        _2827,
        _2828,
        _2829,
        _2830,
        _2831,
        _2832,
        _2833,
        _2834,
        _2835,
        _2836,
        _2837,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2759

    Self = TypeVar("Self", bound="Part")
    CastSelf = TypeVar("CastSelf", bound="Part._Cast_Part")


__docformat__ = "restructuredtext en"
__all__ = ("Part",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Part:
    """Special nested class for casting Part to subclasses."""

    __parent__: "Part"

    @property
    def design_entity(self: "CastSelf") -> "_2452.DesignEntity":
        return self.__parent__._cast(_2452.DesignEntity)

    @property
    def assembly(self: "CastSelf") -> "_2703.Assembly":
        return self.__parent__._cast(_2703.Assembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2704.AbstractAssembly":
        return self.__parent__._cast(_2704.AbstractAssembly)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2705.AbstractShaft":
        from mastapy._private.system_model.part_model import _2705

        return self.__parent__._cast(_2705.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2706.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2706

        return self.__parent__._cast(_2706.AbstractShaftOrHousing)

    @property
    def bearing(self: "CastSelf") -> "_2709.Bearing":
        from mastapy._private.system_model.part_model import _2709

        return self.__parent__._cast(_2709.Bearing)

    @property
    def bolt(self: "CastSelf") -> "_2712.Bolt":
        from mastapy._private.system_model.part_model import _2712

        return self.__parent__._cast(_2712.Bolt)

    @property
    def bolted_joint(self: "CastSelf") -> "_2713.BoltedJoint":
        from mastapy._private.system_model.part_model import _2713

        return self.__parent__._cast(_2713.BoltedJoint)

    @property
    def component(self: "CastSelf") -> "_2715.Component":
        from mastapy._private.system_model.part_model import _2715

        return self.__parent__._cast(_2715.Component)

    @property
    def connector(self: "CastSelf") -> "_2718.Connector":
        from mastapy._private.system_model.part_model import _2718

        return self.__parent__._cast(_2718.Connector)

    @property
    def datum(self: "CastSelf") -> "_2719.Datum":
        from mastapy._private.system_model.part_model import _2719

        return self.__parent__._cast(_2719.Datum)

    @property
    def external_cad_model(self: "CastSelf") -> "_2724.ExternalCADModel":
        from mastapy._private.system_model.part_model import _2724

        return self.__parent__._cast(_2724.ExternalCADModel)

    @property
    def fe_part(self: "CastSelf") -> "_2725.FEPart":
        from mastapy._private.system_model.part_model import _2725

        return self.__parent__._cast(_2725.FEPart)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2726.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2726

        return self.__parent__._cast(_2726.FlexiblePinAssembly)

    @property
    def guide_dxf_model(self: "CastSelf") -> "_2727.GuideDxfModel":
        from mastapy._private.system_model.part_model import _2727

        return self.__parent__._cast(_2727.GuideDxfModel)

    @property
    def mass_disc(self: "CastSelf") -> "_2734.MassDisc":
        from mastapy._private.system_model.part_model import _2734

        return self.__parent__._cast(_2734.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2735.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2735

        return self.__parent__._cast(_2735.MeasurementComponent)

    @property
    def microphone(self: "CastSelf") -> "_2736.Microphone":
        from mastapy._private.system_model.part_model import _2736

        return self.__parent__._cast(_2736.Microphone)

    @property
    def microphone_array(self: "CastSelf") -> "_2737.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2737

        return self.__parent__._cast(_2737.MicrophoneArray)

    @property
    def mountable_component(self: "CastSelf") -> "_2738.MountableComponent":
        from mastapy._private.system_model.part_model import _2738

        return self.__parent__._cast(_2738.MountableComponent)

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
    def root_assembly(self: "CastSelf") -> "_2751.RootAssembly":
        from mastapy._private.system_model.part_model import _2751

        return self.__parent__._cast(_2751.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2753.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2753

        return self.__parent__._cast(_2753.SpecialisedAssembly)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2754.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2754

        return self.__parent__._cast(_2754.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2756.VirtualComponent":
        from mastapy._private.system_model.part_model import _2756

        return self.__parent__._cast(_2756.VirtualComponent)

    @property
    def shaft(self: "CastSelf") -> "_2759.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2759

        return self.__parent__._cast(_2759.Shaft)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2795.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2795

        return self.__parent__._cast(_2795.AGMAGleasonConicalGear)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2796.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2796

        return self.__parent__._cast(_2796.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2797.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2797

        return self.__parent__._cast(_2797.BevelDifferentialGear)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2798.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2798

        return self.__parent__._cast(_2798.BevelDifferentialGearSet)

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
    def bevel_gear_set(self: "CastSelf") -> "_2802.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2802

        return self.__parent__._cast(_2802.BevelGearSet)

    @property
    def concept_gear(self: "CastSelf") -> "_2803.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2803

        return self.__parent__._cast(_2803.ConceptGear)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2804.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2804

        return self.__parent__._cast(_2804.ConceptGearSet)

    @property
    def conical_gear(self: "CastSelf") -> "_2805.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2805

        return self.__parent__._cast(_2805.ConicalGear)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2806.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2806

        return self.__parent__._cast(_2806.ConicalGearSet)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2807.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2807

        return self.__parent__._cast(_2807.CylindricalGear)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2808.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2808

        return self.__parent__._cast(_2808.CylindricalGearSet)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2809.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2809

        return self.__parent__._cast(_2809.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2810.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2810

        return self.__parent__._cast(_2810.FaceGear)

    @property
    def face_gear_set(self: "CastSelf") -> "_2811.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2811

        return self.__parent__._cast(_2811.FaceGearSet)

    @property
    def gear(self: "CastSelf") -> "_2812.Gear":
        from mastapy._private.system_model.part_model.gears import _2812

        return self.__parent__._cast(_2812.Gear)

    @property
    def gear_set(self: "CastSelf") -> "_2814.GearSet":
        from mastapy._private.system_model.part_model.gears import _2814

        return self.__parent__._cast(_2814.GearSet)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2816.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2816

        return self.__parent__._cast(_2816.HypoidGear)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2817.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2817

        return self.__parent__._cast(_2817.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2818.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2818

        return self.__parent__._cast(_2818.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2819.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2819

        return self.__parent__._cast(_2819.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2820.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2820

        return self.__parent__._cast(_2820.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2821.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2821

        return self.__parent__._cast(_2821.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2822.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2822

        return self.__parent__._cast(_2822.KlingelnbergCycloPalloidSpiralBevelGear)

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
    def spiral_bevel_gear(self: "CastSelf") -> "_2826.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2826

        return self.__parent__._cast(_2826.SpiralBevelGear)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2827.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2827

        return self.__parent__._cast(_2827.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2828.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2828

        return self.__parent__._cast(_2828.StraightBevelDiffGear)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2829.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2829

        return self.__parent__._cast(_2829.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2830.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2830

        return self.__parent__._cast(_2830.StraightBevelGear)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2831.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2831

        return self.__parent__._cast(_2831.StraightBevelGearSet)

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
    def worm_gear_set(self: "CastSelf") -> "_2835.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2835

        return self.__parent__._cast(_2835.WormGearSet)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2836.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2836

        return self.__parent__._cast(_2836.ZerolBevelGear)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2837.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2837

        return self.__parent__._cast(_2837.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2851.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2851

        return self.__parent__._cast(_2851.CycloidalAssembly)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2852.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2852

        return self.__parent__._cast(_2852.CycloidalDisc)

    @property
    def ring_pins(self: "CastSelf") -> "_2853.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2853

        return self.__parent__._cast(_2853.RingPins)

    @property
    def belt_drive(self: "CastSelf") -> "_2860.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2860

        return self.__parent__._cast(_2860.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2862.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2862

        return self.__parent__._cast(_2862.Clutch)

    @property
    def clutch_half(self: "CastSelf") -> "_2863.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2863

        return self.__parent__._cast(_2863.ClutchHalf)

    @property
    def concept_coupling(self: "CastSelf") -> "_2865.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2865

        return self.__parent__._cast(_2865.ConceptCoupling)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2866.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2866

        return self.__parent__._cast(_2866.ConceptCouplingHalf)

    @property
    def coupling(self: "CastSelf") -> "_2868.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2868

        return self.__parent__._cast(_2868.Coupling)

    @property
    def coupling_half(self: "CastSelf") -> "_2869.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2869

        return self.__parent__._cast(_2869.CouplingHalf)

    @property
    def cvt(self: "CastSelf") -> "_2871.CVT":
        from mastapy._private.system_model.part_model.couplings import _2871

        return self.__parent__._cast(_2871.CVT)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2872.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2872

        return self.__parent__._cast(_2872.CVTPulley)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2873.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2873

        return self.__parent__._cast(_2873.PartToPartShearCoupling)

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
    def rolling_ring_assembly(self: "CastSelf") -> "_2884.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2884

        return self.__parent__._cast(_2884.RollingRingAssembly)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2885.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2885

        return self.__parent__._cast(_2885.ShaftHubConnection)

    @property
    def spring_damper(self: "CastSelf") -> "_2891.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2891

        return self.__parent__._cast(_2891.SpringDamper)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2892.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2892

        return self.__parent__._cast(_2892.SpringDamperHalf)

    @property
    def synchroniser(self: "CastSelf") -> "_2893.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2893

        return self.__parent__._cast(_2893.Synchroniser)

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
    def torque_converter(self: "CastSelf") -> "_2898.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2898

        return self.__parent__._cast(_2898.TorqueConverter)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2899.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2899

        return self.__parent__._cast(_2899.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2901.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2901

        return self.__parent__._cast(_2901.TorqueConverterTurbine)

    @property
    def part(self: "CastSelf") -> "Part":
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
class Part(_2452.DesignEntity):
    """Part

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def two_d_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def two_d_drawing_full_model(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingFullModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_isometric_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThreeDIsometricView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThreeDView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXyPlaneWithZAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXyPlaneWithZAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXzPlaneWithYAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXzPlaneWithYAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInYzPlaneWithXAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInYzPlaneWithXAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def drawing_number(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DrawingNumber")

        if temp is None:
            return ""

        return temp

    @drawing_number.setter
    @exception_bridge
    @enforce_parameter_types
    def drawing_number(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawingNumber", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def editable_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "EditableName")

        if temp is None:
            return ""

        return temp

    @editable_name.setter
    @exception_bridge
    @enforce_parameter_types
    def editable_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "EditableName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def mass(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mass.setter
    @exception_bridge
    @enforce_parameter_types
    def mass(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Mass", value)

    @property
    @exception_bridge
    def packaging_size_on_x_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PackagingSizeOnXAxis")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def packaging_size_on_y_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PackagingSizeOnYAxis")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def packaging_size_on_z_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PackagingSizeOnZAxis")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def use_script_to_provide_resistive_torque(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseScriptToProvideResistiveTorque")

        if temp is None:
            return False

        return temp

    @use_script_to_provide_resistive_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def use_script_to_provide_resistive_torque(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseScriptToProvideResistiveTorque",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mass_properties_from_design(self: "Self") -> "_1731.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassPropertiesFromDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mass_properties_from_design_including_planetary_duplicates(
        self: "Self",
    ) -> "_1731.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassPropertiesFromDesignIncludingPlanetaryDuplicates"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connections(self: "Self") -> "List[_2532.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def container(self: "Self") -> "_2704.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Container")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def local_connections(self: "Self") -> "List[_2532.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def connections_to(self: "Self", part: "Part") -> "List[_2532.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Args:
            part (mastapy.system_model.part_model.Part)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "ConnectionsTo", part.wrapped if part else None
            )
        )

    @exception_bridge
    @enforce_parameter_types
    def copy_to(self: "Self", container: "_2703.Assembly") -> "Part":
        """mastapy.system_model.part_model.Part

        Args:
            container (mastapy.system_model.part_model.Assembly)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CopyTo", container.wrapped if container else None
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    def create_geometry_export_options(self: "Self") -> "_2502.GeometryExportOptions":
        """mastapy.system_model.import_export.GeometryExportOptions"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateGeometryExportOptions"
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    def delete_connections(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteConnections")

    @property
    def cast_to(self: "Self") -> "_Cast_Part":
        """Cast to another type.

        Returns:
            _Cast_Part
        """
        return _Cast_Part(self)
