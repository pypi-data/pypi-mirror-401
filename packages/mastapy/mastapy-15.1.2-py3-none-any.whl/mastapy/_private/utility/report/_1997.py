"""CustomReportMultiPropertyItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.utility.report import _1998

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportMultiPropertyItem"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings.bearing_results import _2187, _2191, _2199
    from mastapy._private.gears.gear_designs.cylindrical import _1167
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _5043,
        _5047,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3145,
    )
    from mastapy._private.utility.report import _1984, _1991, _1999, _2001, _2008
    from mastapy._private.utility_gui.charts import _2092, _2093

    Self = TypeVar("Self", bound="CustomReportMultiPropertyItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
    )

TItem = TypeVar("TItem", bound="_2001.CustomReportPropertyItem")

__docformat__ = "restructuredtext en"
__all__ = ("CustomReportMultiPropertyItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportMultiPropertyItem:
    """Special nested class for casting CustomReportMultiPropertyItem to subclasses."""

    __parent__: "CustomReportMultiPropertyItem"

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1998.CustomReportMultiPropertyItemBase":
        return self.__parent__._cast(_1998.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1999.CustomReportNameableItem":
        from mastapy._private.utility.report import _1999

        return self.__parent__._cast(_1999.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1991.CustomReportItem":
        from mastapy._private.utility.report import _1991

        return self.__parent__._cast(_1991.CustomReportItem)

    @property
    def shaft_damage_results_table_and_chart(
        self: "CastSelf",
    ) -> "_20.ShaftDamageResultsTableAndChart":
        from mastapy._private.shafts import _20

        return self.__parent__._cast(_20.ShaftDamageResultsTableAndChart)

    @property
    def cylindrical_gear_table_with_mg_charts(
        self: "CastSelf",
    ) -> "_1167.CylindricalGearTableWithMGCharts":
        from mastapy._private.gears.gear_designs.cylindrical import _1167

        return self.__parent__._cast(_1167.CylindricalGearTableWithMGCharts)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1984.CustomReportChart":
        from mastapy._private.utility.report import _1984

        return self.__parent__._cast(_1984.CustomReportChart)

    @property
    def custom_table(self: "CastSelf") -> "_2008.CustomTable":
        from mastapy._private.utility.report import _2008

        return self.__parent__._cast(_2008.CustomTable)

    @property
    def custom_line_chart(self: "CastSelf") -> "_2092.CustomLineChart":
        from mastapy._private.utility_gui.charts import _2092

        return self.__parent__._cast(_2092.CustomLineChart)

    @property
    def custom_table_and_chart(self: "CastSelf") -> "_2093.CustomTableAndChart":
        from mastapy._private.utility_gui.charts import _2093

        return self.__parent__._cast(_2093.CustomTableAndChart)

    @property
    def loaded_ball_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2187.LoadedBallElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2187

        return self.__parent__._cast(_2187.LoadedBallElementChartReporter)

    @property
    def loaded_bearing_temperature_chart(
        self: "CastSelf",
    ) -> "_2191.LoadedBearingTemperatureChart":
        from mastapy._private.bearings.bearing_results import _2191

        return self.__parent__._cast(_2191.LoadedBearingTemperatureChart)

    @property
    def loaded_roller_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2199.LoadedRollerElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2199

        return self.__parent__._cast(_2199.LoadedRollerElementChartReporter)

    @property
    def shaft_system_deflection_sections_report(
        self: "CastSelf",
    ) -> "_3145.ShaftSystemDeflectionSectionsReport":
        from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
            _3145,
        )

        return self.__parent__._cast(_3145.ShaftSystemDeflectionSectionsReport)

    @property
    def campbell_diagram_report(self: "CastSelf") -> "_5043.CampbellDiagramReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _5043,
        )

        return self.__parent__._cast(_5043.CampbellDiagramReport)

    @property
    def per_mode_results_report(self: "CastSelf") -> "_5047.PerModeResultsReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _5047,
        )

        return self.__parent__._cast(_5047.PerModeResultsReport)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "CustomReportMultiPropertyItem":
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
class CustomReportMultiPropertyItem(
    _1998.CustomReportMultiPropertyItemBase, Generic[TItem]
):
    """CustomReportMultiPropertyItem

    This is a mastapy class.

    Generic Types:
        TItem
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportMultiPropertyItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportMultiPropertyItem
        """
        return _Cast_CustomReportMultiPropertyItem(self)
