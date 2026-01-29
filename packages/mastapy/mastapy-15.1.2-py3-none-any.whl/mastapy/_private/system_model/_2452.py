"""DesignEntity"""

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
from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility

_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    from mastapy._private.system_model import _2449
    from mastapy._private.system_model.connections_and_sockets import (
        _2525,
        _2528,
        _2529,
        _2532,
        _2533,
        _2541,
        _2547,
        _2552,
        _2555,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2602,
        _2604,
        _2606,
        _2608,
        _2610,
        _2612,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2595,
        _2598,
        _2601,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2559,
        _2561,
        _2563,
        _2565,
        _2567,
        _2569,
        _2571,
        _2573,
        _2575,
        _2578,
        _2579,
        _2580,
        _2583,
        _2585,
        _2587,
        _2589,
        _2591,
    )
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
        _2743,
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
    from mastapy._private.utility.model_validation import _2021, _2022
    from mastapy._private.utility.scripting import _1969

    Self = TypeVar("Self", bound="DesignEntity")
    CastSelf = TypeVar("CastSelf", bound="DesignEntity._Cast_DesignEntity")


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntity:
    """Special nested class for casting DesignEntity to subclasses."""

    __parent__: "DesignEntity"

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2525.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2525

        return self.__parent__._cast(_2525.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2528.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2528

        return self.__parent__._cast(_2528.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2529.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2529

        return self.__parent__._cast(_2529.CoaxialConnection)

    @property
    def connection(self: "CastSelf") -> "_2532.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2532

        return self.__parent__._cast(_2532.Connection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2533.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2533

        return self.__parent__._cast(_2533.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2541.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2541

        return self.__parent__._cast(_2541.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2547.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2547

        return self.__parent__._cast(_2547.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2552.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2552

        return self.__parent__._cast(_2552.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2555.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2555

        return self.__parent__._cast(_2555.ShaftToMountableComponentConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2559.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2559

        return self.__parent__._cast(_2559.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2561.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2561

        return self.__parent__._cast(_2561.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2563.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2563

        return self.__parent__._cast(_2563.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2565.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2565

        return self.__parent__._cast(_2565.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2567.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2567

        return self.__parent__._cast(_2567.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2569.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2569

        return self.__parent__._cast(_2569.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2571.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2571

        return self.__parent__._cast(_2571.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2573.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2573

        return self.__parent__._cast(_2573.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2575.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2575

        return self.__parent__._cast(_2575.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2578.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2578

        return self.__parent__._cast(_2578.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2579.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2579

        return self.__parent__._cast(_2579.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2580.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2580

        return self.__parent__._cast(_2580.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2583.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2583

        return self.__parent__._cast(_2583.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2585.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2585

        return self.__parent__._cast(_2585.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2587.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2587

        return self.__parent__._cast(_2587.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2589.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2589

        return self.__parent__._cast(_2589.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2591.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2591

        return self.__parent__._cast(_2591.ZerolBevelGearMesh)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2595.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2595,
        )

        return self.__parent__._cast(_2595.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2598.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2598,
        )

        return self.__parent__._cast(_2598.CycloidalDiscPlanetaryBearingConnection)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2601.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2601,
        )

        return self.__parent__._cast(_2601.RingPinsToDiscConnection)

    @property
    def clutch_connection(self: "CastSelf") -> "_2602.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2602,
        )

        return self.__parent__._cast(_2602.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2604.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2604,
        )

        return self.__parent__._cast(_2604.ConceptCouplingConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "_2606.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2606,
        )

        return self.__parent__._cast(_2606.CouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2608.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2608,
        )

        return self.__parent__._cast(_2608.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2610.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2610,
        )

        return self.__parent__._cast(_2610.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2612.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2612,
        )

        return self.__parent__._cast(_2612.TorqueConverterConnection)

    @property
    def assembly(self: "CastSelf") -> "_2703.Assembly":
        from mastapy._private.system_model.part_model import _2703

        return self.__parent__._cast(_2703.Assembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2704.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2704

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
    def part(self: "CastSelf") -> "_2743.Part":
        from mastapy._private.system_model.part_model import _2743

        return self.__parent__._cast(_2743.Part)

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
    def design_entity(self: "CastSelf") -> "DesignEntity":
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
class DesignEntity(_0.APIBase):
    """DesignEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @exception_bridge
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
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
    def id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Icon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def small_icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallIcon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

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
    def design_properties(self: "Self") -> "_2449.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def all_design_entities(self: "Self") -> "List[DesignEntity]":
        """List[mastapy.system_model.DesignEntity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllDesignEntities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def all_status_errors(self: "Self") -> "List[_2022.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllStatusErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def status(self: "Self") -> "_2021.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def user_specified_data(self: "Self") -> "_1969.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntity":
        """Cast to another type.

        Returns:
            _Cast_DesignEntity
        """
        return _Cast_DesignEntity(self)
