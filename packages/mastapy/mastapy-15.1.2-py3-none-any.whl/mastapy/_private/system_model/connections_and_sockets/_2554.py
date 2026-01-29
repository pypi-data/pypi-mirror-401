"""ShaftSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.system_model.connections_and_sockets import _2536

_SHAFT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "ShaftSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2539,
        _2540,
        _2545,
        _2546,
        _2556,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2593,
        _2594,
        _2596,
    )

    Self = TypeVar("Self", bound="ShaftSocket")
    CastSelf = TypeVar("CastSelf", bound="ShaftSocket._Cast_ShaftSocket")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSocket:
    """Special nested class for casting ShaftSocket to subclasses."""

    __parent__: "ShaftSocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2536.CylindricalSocket":
        return self.__parent__._cast(_2536.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2556.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2556

        return self.__parent__._cast(_2556.Socket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2539.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2539

        return self.__parent__._cast(_2539.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2540.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2540

        return self.__parent__._cast(_2540.InnerShaftSocketBase)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2545.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2545

        return self.__parent__._cast(_2545.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2546.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2546

        return self.__parent__._cast(_2546.OuterShaftSocketBase)

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
    def shaft_socket(self: "CastSelf") -> "ShaftSocket":
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
class ShaftSocket(_2536.CylindricalSocket):
    """ShaftSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSocket":
        """Cast to another type.

        Returns:
            _Cast_ShaftSocket
        """
        return _Cast_ShaftSocket(self)
