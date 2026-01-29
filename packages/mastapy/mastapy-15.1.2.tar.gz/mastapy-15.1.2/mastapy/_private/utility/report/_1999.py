"""CustomReportNameableItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

from mastapy._private._internal import utility
from mastapy._private.utility.report import _1991

_CUSTOM_REPORT_NAMEABLE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportNameableItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2187, _2188, _2191, _2199
    from mastapy._private.gears.gear_designs.cylindrical import _1167
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _5043,
        _5047,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4706,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3145,
    )
    from mastapy._private.utility.report import (
        _1970,
        _1978,
        _1979,
        _1980,
        _1981,
        _1983,
        _1984,
        _1988,
        _1990,
        _1997,
        _1998,
        _2000,
        _2002,
        _2005,
        _2007,
        _2008,
        _2010,
    )
    from mastapy._private.utility_gui.charts import _2092, _2093

    Self = TypeVar("Self", bound="CustomReportNameableItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportNameableItem._Cast_CustomReportNameableItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportNameableItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportNameableItem:
    """Special nested class for casting CustomReportNameableItem to subclasses."""

    __parent__: "CustomReportNameableItem"

    @property
    def custom_report_item(self: "CastSelf") -> "_1991.CustomReportItem":
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
    def ad_hoc_custom_table(self: "CastSelf") -> "_1970.AdHocCustomTable":
        from mastapy._private.utility.report import _1970

        return self.__parent__._cast(_1970.AdHocCustomTable)

    @property
    def custom_chart(self: "CastSelf") -> "_1978.CustomChart":
        from mastapy._private.utility.report import _1978

        return self.__parent__._cast(_1978.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1979.CustomDrawing":
        from mastapy._private.utility.report import _1979

        return self.__parent__._cast(_1979.CustomDrawing)

    @property
    def custom_graphic(self: "CastSelf") -> "_1980.CustomGraphic":
        from mastapy._private.utility.report import _1980

        return self.__parent__._cast(_1980.CustomGraphic)

    @property
    def custom_image(self: "CastSelf") -> "_1981.CustomImage":
        from mastapy._private.utility.report import _1981

        return self.__parent__._cast(_1981.CustomImage)

    @property
    def custom_report_cad_drawing(self: "CastSelf") -> "_1983.CustomReportCadDrawing":
        from mastapy._private.utility.report import _1983

        return self.__parent__._cast(_1983.CustomReportCadDrawing)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1984.CustomReportChart":
        from mastapy._private.utility.report import _1984

        return self.__parent__._cast(_1984.CustomReportChart)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1988.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1988

        return self.__parent__._cast(_1988.CustomReportDefinitionItem)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1990.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1990

        return self.__parent__._cast(_1990.CustomReportHtmlItem)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1997.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1997

        return self.__parent__._cast(_1997.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1998.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1998

        return self.__parent__._cast(_1998.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_named_item(self: "CastSelf") -> "_2000.CustomReportNamedItem":
        from mastapy._private.utility.report import _2000

        return self.__parent__._cast(_2000.CustomReportNamedItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_2002.CustomReportStatusItem":
        from mastapy._private.utility.report import _2002

        return self.__parent__._cast(_2002.CustomReportStatusItem)

    @property
    def custom_report_text(self: "CastSelf") -> "_2005.CustomReportText":
        from mastapy._private.utility.report import _2005

        return self.__parent__._cast(_2005.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_2007.CustomSubReport":
        from mastapy._private.utility.report import _2007

        return self.__parent__._cast(_2007.CustomSubReport)

    @property
    def custom_table(self: "CastSelf") -> "_2008.CustomTable":
        from mastapy._private.utility.report import _2008

        return self.__parent__._cast(_2008.CustomTable)

    @property
    def dynamic_custom_report_item(self: "CastSelf") -> "_2010.DynamicCustomReportItem":
        from mastapy._private.utility.report import _2010

        return self.__parent__._cast(_2010.DynamicCustomReportItem)

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
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2188.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2188

        return self.__parent__._cast(_2188.LoadedBearingChartReporter)

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
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4706.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4706,
        )

        return self.__parent__._cast(_4706.ParametricStudyHistogram)

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
    def custom_report_nameable_item(self: "CastSelf") -> "CustomReportNameableItem":
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
class CustomReportNameableItem(_1991.CustomReportItem):
    """CustomReportNameableItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_NAMEABLE_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def x_position_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "XPositionForCAD")

        if temp is None:
            return 0.0

        return temp

    @x_position_for_cad.setter
    @exception_bridge
    @enforce_parameter_types
    def x_position_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "XPositionForCAD", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def y_position_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "YPositionForCAD")

        if temp is None:
            return 0.0

        return temp

    @y_position_for_cad.setter
    @exception_bridge
    @enforce_parameter_types
    def y_position_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "YPositionForCAD", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportNameableItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportNameableItem
        """
        return _Cast_CustomReportNameableItem(self)
