"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.report._1970 import AdHocCustomTable
    from mastapy._private.utility.report._1971 import AxisSettings
    from mastapy._private.utility.report._1972 import BlankRow
    from mastapy._private.utility.report._1973 import CadPageOrientation
    from mastapy._private.utility.report._1974 import CadPageSize
    from mastapy._private.utility.report._1975 import CadTableBorderType
    from mastapy._private.utility.report._1976 import ChartDefinition
    from mastapy._private.utility.report._1977 import SMTChartPointShape
    from mastapy._private.utility.report._1978 import CustomChart
    from mastapy._private.utility.report._1979 import CustomDrawing
    from mastapy._private.utility.report._1980 import CustomGraphic
    from mastapy._private.utility.report._1981 import CustomImage
    from mastapy._private.utility.report._1982 import CustomReport
    from mastapy._private.utility.report._1983 import CustomReportCadDrawing
    from mastapy._private.utility.report._1984 import CustomReportChart
    from mastapy._private.utility.report._1985 import CustomReportChartItem
    from mastapy._private.utility.report._1986 import CustomReportColumn
    from mastapy._private.utility.report._1987 import CustomReportColumns
    from mastapy._private.utility.report._1988 import CustomReportDefinitionItem
    from mastapy._private.utility.report._1989 import CustomReportHorizontalLine
    from mastapy._private.utility.report._1990 import CustomReportHtmlItem
    from mastapy._private.utility.report._1991 import CustomReportItem
    from mastapy._private.utility.report._1992 import CustomReportItemContainer
    from mastapy._private.utility.report._1993 import (
        CustomReportItemContainerCollection,
    )
    from mastapy._private.utility.report._1994 import (
        CustomReportItemContainerCollectionBase,
    )
    from mastapy._private.utility.report._1995 import (
        CustomReportItemContainerCollectionItem,
    )
    from mastapy._private.utility.report._1996 import CustomReportKey
    from mastapy._private.utility.report._1997 import CustomReportMultiPropertyItem
    from mastapy._private.utility.report._1998 import CustomReportMultiPropertyItemBase
    from mastapy._private.utility.report._1999 import CustomReportNameableItem
    from mastapy._private.utility.report._2000 import CustomReportNamedItem
    from mastapy._private.utility.report._2001 import CustomReportPropertyItem
    from mastapy._private.utility.report._2002 import CustomReportStatusItem
    from mastapy._private.utility.report._2003 import CustomReportTab
    from mastapy._private.utility.report._2004 import CustomReportTabs
    from mastapy._private.utility.report._2005 import CustomReportText
    from mastapy._private.utility.report._2006 import CustomRow
    from mastapy._private.utility.report._2007 import CustomSubReport
    from mastapy._private.utility.report._2008 import CustomTable
    from mastapy._private.utility.report._2009 import DefinitionBooleanCheckOptions
    from mastapy._private.utility.report._2010 import DynamicCustomReportItem
    from mastapy._private.utility.report._2011 import FontStyle
    from mastapy._private.utility.report._2012 import FontWeight
    from mastapy._private.utility.report._2013 import HeadingSize
    from mastapy._private.utility.report._2014 import SimpleChartDefinition
    from mastapy._private.utility.report._2015 import UserTextRow
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.report._1970": ["AdHocCustomTable"],
        "_private.utility.report._1971": ["AxisSettings"],
        "_private.utility.report._1972": ["BlankRow"],
        "_private.utility.report._1973": ["CadPageOrientation"],
        "_private.utility.report._1974": ["CadPageSize"],
        "_private.utility.report._1975": ["CadTableBorderType"],
        "_private.utility.report._1976": ["ChartDefinition"],
        "_private.utility.report._1977": ["SMTChartPointShape"],
        "_private.utility.report._1978": ["CustomChart"],
        "_private.utility.report._1979": ["CustomDrawing"],
        "_private.utility.report._1980": ["CustomGraphic"],
        "_private.utility.report._1981": ["CustomImage"],
        "_private.utility.report._1982": ["CustomReport"],
        "_private.utility.report._1983": ["CustomReportCadDrawing"],
        "_private.utility.report._1984": ["CustomReportChart"],
        "_private.utility.report._1985": ["CustomReportChartItem"],
        "_private.utility.report._1986": ["CustomReportColumn"],
        "_private.utility.report._1987": ["CustomReportColumns"],
        "_private.utility.report._1988": ["CustomReportDefinitionItem"],
        "_private.utility.report._1989": ["CustomReportHorizontalLine"],
        "_private.utility.report._1990": ["CustomReportHtmlItem"],
        "_private.utility.report._1991": ["CustomReportItem"],
        "_private.utility.report._1992": ["CustomReportItemContainer"],
        "_private.utility.report._1993": ["CustomReportItemContainerCollection"],
        "_private.utility.report._1994": ["CustomReportItemContainerCollectionBase"],
        "_private.utility.report._1995": ["CustomReportItemContainerCollectionItem"],
        "_private.utility.report._1996": ["CustomReportKey"],
        "_private.utility.report._1997": ["CustomReportMultiPropertyItem"],
        "_private.utility.report._1998": ["CustomReportMultiPropertyItemBase"],
        "_private.utility.report._1999": ["CustomReportNameableItem"],
        "_private.utility.report._2000": ["CustomReportNamedItem"],
        "_private.utility.report._2001": ["CustomReportPropertyItem"],
        "_private.utility.report._2002": ["CustomReportStatusItem"],
        "_private.utility.report._2003": ["CustomReportTab"],
        "_private.utility.report._2004": ["CustomReportTabs"],
        "_private.utility.report._2005": ["CustomReportText"],
        "_private.utility.report._2006": ["CustomRow"],
        "_private.utility.report._2007": ["CustomSubReport"],
        "_private.utility.report._2008": ["CustomTable"],
        "_private.utility.report._2009": ["DefinitionBooleanCheckOptions"],
        "_private.utility.report._2010": ["DynamicCustomReportItem"],
        "_private.utility.report._2011": ["FontStyle"],
        "_private.utility.report._2012": ["FontWeight"],
        "_private.utility.report._2013": ["HeadingSize"],
        "_private.utility.report._2014": ["SimpleChartDefinition"],
        "_private.utility.report._2015": ["UserTextRow"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdHocCustomTable",
    "AxisSettings",
    "BlankRow",
    "CadPageOrientation",
    "CadPageSize",
    "CadTableBorderType",
    "ChartDefinition",
    "SMTChartPointShape",
    "CustomChart",
    "CustomDrawing",
    "CustomGraphic",
    "CustomImage",
    "CustomReport",
    "CustomReportCadDrawing",
    "CustomReportChart",
    "CustomReportChartItem",
    "CustomReportColumn",
    "CustomReportColumns",
    "CustomReportDefinitionItem",
    "CustomReportHorizontalLine",
    "CustomReportHtmlItem",
    "CustomReportItem",
    "CustomReportItemContainer",
    "CustomReportItemContainerCollection",
    "CustomReportItemContainerCollectionBase",
    "CustomReportItemContainerCollectionItem",
    "CustomReportKey",
    "CustomReportMultiPropertyItem",
    "CustomReportMultiPropertyItemBase",
    "CustomReportNameableItem",
    "CustomReportNamedItem",
    "CustomReportPropertyItem",
    "CustomReportStatusItem",
    "CustomReportTab",
    "CustomReportTabs",
    "CustomReportText",
    "CustomRow",
    "CustomSubReport",
    "CustomTable",
    "DefinitionBooleanCheckOptions",
    "DynamicCustomReportItem",
    "FontStyle",
    "FontWeight",
    "HeadingSize",
    "SimpleChartDefinition",
    "UserTextRow",
)
