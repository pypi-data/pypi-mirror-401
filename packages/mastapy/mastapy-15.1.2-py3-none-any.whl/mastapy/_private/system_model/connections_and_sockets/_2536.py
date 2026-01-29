"""CylindricalSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.connections_and_sockets import _2556

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2526,
        _2527,
        _2534,
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
    from mastapy._private.system_model.connections_and_sockets.gears import _2570

    Self = TypeVar("Self", bound="CylindricalSocket")
    CastSelf = TypeVar("CastSelf", bound="CylindricalSocket._Cast_CylindricalSocket")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSocket:
    """Special nested class for casting CylindricalSocket to subclasses."""

    __parent__: "CylindricalSocket"

    @property
    def socket(self: "CastSelf") -> "_2556.Socket":
        return self.__parent__._cast(_2556.Socket)

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
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2570.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2570

        return self.__parent__._cast(_2570.CylindricalGearTeethSocket)

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
    def cylindrical_socket(self: "CastSelf") -> "CylindricalSocket":
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
class CylindricalSocket(_2556.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSocket":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSocket
        """
        return _Cast_CylindricalSocket(self)
