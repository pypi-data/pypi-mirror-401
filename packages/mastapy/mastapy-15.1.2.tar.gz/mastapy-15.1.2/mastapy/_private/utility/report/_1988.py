"""CustomReportDefinitionItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

from mastapy._private._internal import utility
from mastapy._private.utility.report import _1999

_CUSTOM_REPORT_DEFINITION_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportDefinitionItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2188
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4706,
    )
    from mastapy._private.utility.report import (
        _1970,
        _1978,
        _1979,
        _1980,
        _1981,
        _1990,
        _1991,
        _2002,
        _2005,
        _2007,
    )

    Self = TypeVar("Self", bound="CustomReportDefinitionItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportDefinitionItem._Cast_CustomReportDefinitionItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportDefinitionItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportDefinitionItem:
    """Special nested class for casting CustomReportDefinitionItem to subclasses."""

    __parent__: "CustomReportDefinitionItem"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1999.CustomReportNameableItem":
        return self.__parent__._cast(_1999.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1991.CustomReportItem":
        from mastapy._private.utility.report import _1991

        return self.__parent__._cast(_1991.CustomReportItem)

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
    def custom_report_html_item(self: "CastSelf") -> "_1990.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1990

        return self.__parent__._cast(_1990.CustomReportHtmlItem)

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
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2188.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2188

        return self.__parent__._cast(_2188.LoadedBearingChartReporter)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4706.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4706,
        )

        return self.__parent__._cast(_4706.ParametricStudyHistogram)

    @property
    def custom_report_definition_item(self: "CastSelf") -> "CustomReportDefinitionItem":
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
class CustomReportDefinitionItem(_1999.CustomReportNameableItem):
    """CustomReportDefinitionItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_DEFINITION_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportDefinitionItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportDefinitionItem
        """
        return _Cast_CustomReportDefinitionItem(self)
