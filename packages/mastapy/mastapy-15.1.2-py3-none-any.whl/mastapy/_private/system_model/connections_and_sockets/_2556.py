"""Socket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2526,
        _2527,
        _2532,
        _2534,
        _2536,
        _2538,
        _2539,
        _2540,
        _2542,
        _2543,
        _2544,
        _2545,
        _2546,
        _2548,
        _2549,
        _2550,
        _2553,
        _2554,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2603,
        _2605,
        _2607,
        _2609,
        _2611,
        _2613,
        _2614,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2593,
        _2594,
        _2596,
        _2597,
        _2599,
        _2600,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2560,
        _2562,
        _2564,
        _2566,
        _2568,
        _2570,
        _2572,
        _2574,
        _2576,
        _2577,
        _2581,
        _2582,
        _2584,
        _2586,
        _2588,
        _2590,
        _2592,
    )
    from mastapy._private.system_model.part_model import _2715, _2716

    Self = TypeVar("Self", bound="Socket")
    CastSelf = TypeVar("CastSelf", bound="Socket._Cast_Socket")


__docformat__ = "restructuredtext en"
__all__ = ("Socket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Socket:
    """Special nested class for casting Socket to subclasses."""

    __parent__: "Socket"

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2526.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2526

        return self.__parent__._cast(_2526.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2527.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2527

        return self.__parent__._cast(_2527.BearingOuterSocket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2534.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2534

        return self.__parent__._cast(_2534.CVTPulleySocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2536.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2536

        return self.__parent__._cast(_2536.CylindricalSocket)

    @property
    def electric_machine_stator_socket(
        self: "CastSelf",
    ) -> "_2538.ElectricMachineStatorSocket":
        from mastapy._private.system_model.connections_and_sockets import _2538

        return self.__parent__._cast(_2538.ElectricMachineStatorSocket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2539.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2539

        return self.__parent__._cast(_2539.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2540.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2540

        return self.__parent__._cast(_2540.InnerShaftSocketBase)

    @property
    def mountable_component_inner_socket(
        self: "CastSelf",
    ) -> "_2542.MountableComponentInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2542

        return self.__parent__._cast(_2542.MountableComponentInnerSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2543.MountableComponentOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2543

        return self.__parent__._cast(_2543.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2544.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2544

        return self.__parent__._cast(_2544.MountableComponentSocket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2545.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2545

        return self.__parent__._cast(_2545.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2546.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2546

        return self.__parent__._cast(_2546.OuterShaftSocketBase)

    @property
    def planetary_socket(self: "CastSelf") -> "_2548.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2548

        return self.__parent__._cast(_2548.PlanetarySocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2549.PlanetarySocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2549

        return self.__parent__._cast(_2549.PlanetarySocketBase)

    @property
    def pulley_socket(self: "CastSelf") -> "_2550.PulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2550

        return self.__parent__._cast(_2550.PulleySocket)

    @property
    def rolling_ring_socket(self: "CastSelf") -> "_2553.RollingRingSocket":
        from mastapy._private.system_model.connections_and_sockets import _2553

        return self.__parent__._cast(_2553.RollingRingSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "_2554.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2554

        return self.__parent__._cast(_2554.ShaftSocket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2560.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2560

        return self.__parent__._cast(_2560.AGMAGleasonConicalGearTeethSocket)

    @property
    def bevel_differential_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2562.BevelDifferentialGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2562

        return self.__parent__._cast(_2562.BevelDifferentialGearTeethSocket)

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2564.BevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2564

        return self.__parent__._cast(_2564.BevelGearTeethSocket)

    @property
    def concept_gear_teeth_socket(self: "CastSelf") -> "_2566.ConceptGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2566

        return self.__parent__._cast(_2566.ConceptGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2568.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2568

        return self.__parent__._cast(_2568.ConicalGearTeethSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2570.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2570

        return self.__parent__._cast(_2570.CylindricalGearTeethSocket)

    @property
    def face_gear_teeth_socket(self: "CastSelf") -> "_2572.FaceGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2572

        return self.__parent__._cast(_2572.FaceGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2574.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2574

        return self.__parent__._cast(_2574.GearTeethSocket)

    @property
    def hypoid_gear_teeth_socket(self: "CastSelf") -> "_2576.HypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2576

        return self.__parent__._cast(_2576.HypoidGearTeethSocket)

    @property
    def klingelnberg_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2577.KlingelnbergConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2577

        return self.__parent__._cast(_2577.KlingelnbergConicalGearTeethSocket)

    @property
    def klingelnberg_hypoid_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2581.KlingelnbergHypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2581

        return self.__parent__._cast(_2581.KlingelnbergHypoidGearTeethSocket)

    @property
    def klingelnberg_spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2582.KlingelnbergSpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2582

        return self.__parent__._cast(_2582.KlingelnbergSpiralBevelGearTeethSocket)

    @property
    def spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2584.SpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2584

        return self.__parent__._cast(_2584.SpiralBevelGearTeethSocket)

    @property
    def straight_bevel_diff_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2586.StraightBevelDiffGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2586

        return self.__parent__._cast(_2586.StraightBevelDiffGearTeethSocket)

    @property
    def straight_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2588.StraightBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2588

        return self.__parent__._cast(_2588.StraightBevelGearTeethSocket)

    @property
    def worm_gear_teeth_socket(self: "CastSelf") -> "_2590.WormGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2590

        return self.__parent__._cast(_2590.WormGearTeethSocket)

    @property
    def zerol_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2592.ZerolBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2592

        return self.__parent__._cast(_2592.ZerolBevelGearTeethSocket)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2593.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2593,
        )

        return self.__parent__._cast(_2593.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2594.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2594,
        )

        return self.__parent__._cast(_2594.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2596.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2596,
        )

        return self.__parent__._cast(_2596.CycloidalDiscInnerSocket)

    @property
    def cycloidal_disc_outer_socket(
        self: "CastSelf",
    ) -> "_2597.CycloidalDiscOuterSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2597,
        )

        return self.__parent__._cast(_2597.CycloidalDiscOuterSocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2599.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2599,
        )

        return self.__parent__._cast(_2599.CycloidalDiscPlanetaryBearingSocket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "_2600.RingPinsSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2600,
        )

        return self.__parent__._cast(_2600.RingPinsSocket)

    @property
    def clutch_socket(self: "CastSelf") -> "_2603.ClutchSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2603,
        )

        return self.__parent__._cast(_2603.ClutchSocket)

    @property
    def concept_coupling_socket(self: "CastSelf") -> "_2605.ConceptCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2605,
        )

        return self.__parent__._cast(_2605.ConceptCouplingSocket)

    @property
    def coupling_socket(self: "CastSelf") -> "_2607.CouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2607,
        )

        return self.__parent__._cast(_2607.CouplingSocket)

    @property
    def part_to_part_shear_coupling_socket(
        self: "CastSelf",
    ) -> "_2609.PartToPartShearCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2609,
        )

        return self.__parent__._cast(_2609.PartToPartShearCouplingSocket)

    @property
    def spring_damper_socket(self: "CastSelf") -> "_2611.SpringDamperSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2611,
        )

        return self.__parent__._cast(_2611.SpringDamperSocket)

    @property
    def torque_converter_pump_socket(
        self: "CastSelf",
    ) -> "_2613.TorqueConverterPumpSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2613,
        )

        return self.__parent__._cast(_2613.TorqueConverterPumpSocket)

    @property
    def torque_converter_turbine_socket(
        self: "CastSelf",
    ) -> "_2614.TorqueConverterTurbineSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2614,
        )

        return self.__parent__._cast(_2614.TorqueConverterTurbineSocket)

    @property
    def socket(self: "CastSelf") -> "Socket":
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
class Socket(_0.APIBase):
    """Socket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def connected_components(self: "Self") -> "List[_2715.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def owner(self: "Self") -> "_2715.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Owner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def connect_to(
        self: "Self", component: "_2715.Component"
    ) -> "_2716.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ConnectTo",
            [_COMPONENT],
            component.wrapped if component else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def connect_to_socket(
        self: "Self", socket: "Socket"
    ) -> "_2716.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "ConnectTo", [_SOCKET], socket.wrapped if socket else None
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def connection_to(self: "Self", socket: "Socket") -> "_2532.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "ConnectionTo", socket.wrapped if socket else None
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def get_possible_sockets_to_connect_to(
        self: "Self", component_to_connect_to: "_2715.Component"
    ) -> "List[Socket]":
        """List[mastapy.system_model.connections_and_sockets.Socket]

        Args:
            component_to_connect_to (mastapy.system_model.part_model.Component)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped,
                "GetPossibleSocketsToConnectTo",
                component_to_connect_to.wrapped if component_to_connect_to else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Socket":
        """Cast to another type.

        Returns:
            _Cast_Socket
        """
        return _Cast_Socket(self)
