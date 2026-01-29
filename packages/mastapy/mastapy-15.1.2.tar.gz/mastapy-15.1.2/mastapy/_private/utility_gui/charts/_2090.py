"""BubbleChartDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.utility_gui.charts import _2100

_BUBBLE_CHART_DEFINITION = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "BubbleChartDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1976
    from mastapy._private.utility_gui.charts import _2097, _2105

    Self = TypeVar("Self", bound="BubbleChartDefinition")
    CastSelf = TypeVar(
        "CastSelf", bound="BubbleChartDefinition._Cast_BubbleChartDefinition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BubbleChartDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BubbleChartDefinition:
    """Special nested class for casting BubbleChartDefinition to subclasses."""

    __parent__: "BubbleChartDefinition"

    @property
    def scatter_chart_definition(self: "CastSelf") -> "_2100.ScatterChartDefinition":
        return self.__parent__._cast(_2100.ScatterChartDefinition)

    @property
    def two_d_chart_definition(self: "CastSelf") -> "_2105.TwoDChartDefinition":
        from mastapy._private.utility_gui.charts import _2105

        return self.__parent__._cast(_2105.TwoDChartDefinition)

    @property
    def nd_chart_definition(self: "CastSelf") -> "_2097.NDChartDefinition":
        from mastapy._private.utility_gui.charts import _2097

        return self.__parent__._cast(_2097.NDChartDefinition)

    @property
    def chart_definition(self: "CastSelf") -> "_1976.ChartDefinition":
        from mastapy._private.utility.report import _1976

        return self.__parent__._cast(_1976.ChartDefinition)

    @property
    def bubble_chart_definition(self: "CastSelf") -> "BubbleChartDefinition":
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
class BubbleChartDefinition(_2100.ScatterChartDefinition):
    """BubbleChartDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BUBBLE_CHART_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BubbleChartDefinition":
        """Cast to another type.

        Returns:
            _Cast_BubbleChartDefinition
        """
        return _Cast_BubbleChartDefinition(self)
