"""CVTBeltConnectionLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

from mastapy._private._internal import constructor, utility
from mastapy._private.system_model.analyses_and_results.static_loads import _7742

_CVT_BELT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CVTBeltConnectionLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2942, _2944, _2946
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7771,
        _7833,
    )
    from mastapy._private.system_model.connections_and_sockets import _2533

    Self = TypeVar("Self", bound="CVTBeltConnectionLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CVTBeltConnectionLoadCase._Cast_CVTBeltConnectionLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTBeltConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTBeltConnectionLoadCase:
    """Special nested class for casting CVTBeltConnectionLoadCase to subclasses."""

    __parent__: "CVTBeltConnectionLoadCase"

    @property
    def belt_connection_load_case(self: "CastSelf") -> "_7742.BeltConnectionLoadCase":
        return self.__parent__._cast(_7742.BeltConnectionLoadCase)

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7833.InterMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7833,
        )

        return self.__parent__._cast(_7833.InterMountableComponentConnectionLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_7771.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7771,
        )

        return self.__parent__._cast(_7771.ConnectionLoadCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2942.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2942

        return self.__parent__._cast(_2942.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2946.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2946

        return self.__parent__._cast(_2946.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2944.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2944

        return self.__parent__._cast(_2944.DesignEntityAnalysis)

    @property
    def cvt_belt_connection_load_case(self: "CastSelf") -> "CVTBeltConnectionLoadCase":
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
class CVTBeltConnectionLoadCase(_7742.BeltConnectionLoadCase):
    """CVTBeltConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_BELT_CONNECTION_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2533.CVTBeltConnection":
        """mastapy.system_model.connections_and_sockets.CVTBeltConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CVTBeltConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CVTBeltConnectionLoadCase
        """
        return _Cast_CVTBeltConnectionLoadCase(self)
