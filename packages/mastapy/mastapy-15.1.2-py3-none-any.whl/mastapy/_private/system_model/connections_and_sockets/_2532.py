"""Connection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private.system_model import _2452

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2525,
        _2528,
        _2529,
        _2533,
        _2541,
        _2547,
        _2552,
        _2555,
        _2556,
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
    from mastapy._private.system_model.part_model import _2715

    Self = TypeVar("Self", bound="Connection")
    CastSelf = TypeVar("CastSelf", bound="Connection._Cast_Connection")


__docformat__ = "restructuredtext en"
__all__ = ("Connection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Connection:
    """Special nested class for casting Connection to subclasses."""

    __parent__: "Connection"

    @property
    def design_entity(self: "CastSelf") -> "_2452.DesignEntity":
        return self.__parent__._cast(_2452.DesignEntity)

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
    def connection(self: "CastSelf") -> "Connection":
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
class Connection(_2452.DesignEntity):
    """Connection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionID")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def drawing_position(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DrawingPosition")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @drawing_position.setter
    @exception_bridge
    @enforce_parameter_types
    def drawing_position(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DrawingPosition", value)

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
    def speed_ratio_from_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedRatioFromAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_ratio_from_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatioFromAToB")

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
    def owner_a(self: "Self") -> "_2715.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OwnerA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def owner_b(self: "Self") -> "_2715.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OwnerB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def socket_a(self: "Self") -> "_2556.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def socket_b(self: "Self") -> "_2556.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def other_owner(self: "Self", component: "_2715.Component") -> "_2715.Component":
        """mastapy.system_model.part_model.Component

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "OtherOwner", component.wrapped if component else None
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def other_socket_for_component(
        self: "Self", component: "_2715.Component"
    ) -> "_2556.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "OtherSocket",
            [_COMPONENT],
            component.wrapped if component else None,
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def other_socket(self: "Self", socket: "_2556.Socket") -> "_2556.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "OtherSocket", [_SOCKET], socket.wrapped if socket else None
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @exception_bridge
    @enforce_parameter_types
    def socket_for(self: "Self", component: "_2715.Component") -> "_2556.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "SocketFor", component.wrapped if component else None
        )
        if method_result is None:
            return None

        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result)

    @property
    def cast_to(self: "Self") -> "_Cast_Connection":
        """Cast to another type.

        Returns:
            _Cast_Connection
        """
        return _Cast_Connection(self)
