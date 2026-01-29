"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility_gui.charts._2090 import BubbleChartDefinition
    from mastapy._private.utility_gui.charts._2091 import ConstantLine
    from mastapy._private.utility_gui.charts._2092 import CustomLineChart
    from mastapy._private.utility_gui.charts._2093 import CustomTableAndChart
    from mastapy._private.utility_gui.charts._2094 import LegacyChartMathChartDefinition
    from mastapy._private.utility_gui.charts._2095 import MatrixVisualisationDefinition
    from mastapy._private.utility_gui.charts._2096 import ModeConstantLine
    from mastapy._private.utility_gui.charts._2097 import NDChartDefinition
    from mastapy._private.utility_gui.charts._2098 import (
        ParallelCoordinatesChartDefinition,
    )
    from mastapy._private.utility_gui.charts._2099 import PointsForSurface
    from mastapy._private.utility_gui.charts._2100 import ScatterChartDefinition
    from mastapy._private.utility_gui.charts._2101 import Series2D
    from mastapy._private.utility_gui.charts._2102 import SMTAxis
    from mastapy._private.utility_gui.charts._2103 import ThreeDChartDefinition
    from mastapy._private.utility_gui.charts._2104 import ThreeDVectorChartDefinition
    from mastapy._private.utility_gui.charts._2105 import TwoDChartDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility_gui.charts._2090": ["BubbleChartDefinition"],
        "_private.utility_gui.charts._2091": ["ConstantLine"],
        "_private.utility_gui.charts._2092": ["CustomLineChart"],
        "_private.utility_gui.charts._2093": ["CustomTableAndChart"],
        "_private.utility_gui.charts._2094": ["LegacyChartMathChartDefinition"],
        "_private.utility_gui.charts._2095": ["MatrixVisualisationDefinition"],
        "_private.utility_gui.charts._2096": ["ModeConstantLine"],
        "_private.utility_gui.charts._2097": ["NDChartDefinition"],
        "_private.utility_gui.charts._2098": ["ParallelCoordinatesChartDefinition"],
        "_private.utility_gui.charts._2099": ["PointsForSurface"],
        "_private.utility_gui.charts._2100": ["ScatterChartDefinition"],
        "_private.utility_gui.charts._2101": ["Series2D"],
        "_private.utility_gui.charts._2102": ["SMTAxis"],
        "_private.utility_gui.charts._2103": ["ThreeDChartDefinition"],
        "_private.utility_gui.charts._2104": ["ThreeDVectorChartDefinition"],
        "_private.utility_gui.charts._2105": ["TwoDChartDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BubbleChartDefinition",
    "ConstantLine",
    "CustomLineChart",
    "CustomTableAndChart",
    "LegacyChartMathChartDefinition",
    "MatrixVisualisationDefinition",
    "ModeConstantLine",
    "NDChartDefinition",
    "ParallelCoordinatesChartDefinition",
    "PointsForSurface",
    "ScatterChartDefinition",
    "Series2D",
    "SMTAxis",
    "ThreeDChartDefinition",
    "ThreeDVectorChartDefinition",
    "TwoDChartDefinition",
)
