"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility._1702 import AcousticWeighting
    from mastapy._private.math_utility._1703 import AlignmentAxis
    from mastapy._private.math_utility._1704 import Axis
    from mastapy._private.math_utility._1705 import CirclesOnAxis
    from mastapy._private.math_utility._1706 import ComplexMatrix
    from mastapy._private.math_utility._1707 import ComplexPartDisplayOption
    from mastapy._private.math_utility._1708 import ComplexVector
    from mastapy._private.math_utility._1709 import ComplexVector3D
    from mastapy._private.math_utility._1710 import ComplexVector6D
    from mastapy._private.math_utility._1711 import CoordinateSystem3D
    from mastapy._private.math_utility._1712 import CoordinateSystemEditor
    from mastapy._private.math_utility._1713 import CoordinateSystemForRotation
    from mastapy._private.math_utility._1714 import CoordinateSystemForRotationOrigin
    from mastapy._private.math_utility._1715 import DataPrecision
    from mastapy._private.math_utility._1716 import DegreeOfFreedom
    from mastapy._private.math_utility._1717 import DynamicsResponseScalarResult
    from mastapy._private.math_utility._1718 import DynamicsResponseScaling
    from mastapy._private.math_utility._1719 import EdgeNamedSelectionDetails
    from mastapy._private.math_utility._1720 import Eigenmode
    from mastapy._private.math_utility._1721 import Eigenmodes
    from mastapy._private.math_utility._1722 import EulerParameters
    from mastapy._private.math_utility._1723 import ExtrapolationOptions
    from mastapy._private.math_utility._1724 import FacetedBody
    from mastapy._private.math_utility._1725 import FacetedSurface
    from mastapy._private.math_utility._1726 import FourierSeries
    from mastapy._private.math_utility._1727 import GenericMatrix
    from mastapy._private.math_utility._1728 import GriddedSurface
    from mastapy._private.math_utility._1729 import HarmonicValue
    from mastapy._private.math_utility._1730 import InertiaTensor
    from mastapy._private.math_utility._1731 import MassProperties
    from mastapy._private.math_utility._1732 import MaxMinMean
    from mastapy._private.math_utility._1733 import ComplexMagnitudeMethod
    from mastapy._private.math_utility._1734 import MultipleFourierSeriesInterpolator
    from mastapy._private.math_utility._1735 import Named2DLocation
    from mastapy._private.math_utility._1736 import NamedSelection
    from mastapy._private.math_utility._1737 import NamedSelectionEdge
    from mastapy._private.math_utility._1738 import NamedSelectionFace
    from mastapy._private.math_utility._1739 import NamedSelections
    from mastapy._private.math_utility._1740 import PIDControlUpdateMethod
    from mastapy._private.math_utility._1741 import Quaternion
    from mastapy._private.math_utility._1742 import RealMatrix
    from mastapy._private.math_utility._1743 import RealVector
    from mastapy._private.math_utility._1744 import ResultOptionsFor3DVector
    from mastapy._private.math_utility._1745 import RotationAxis
    from mastapy._private.math_utility._1746 import RoundedOrder
    from mastapy._private.math_utility._1747 import SinCurve
    from mastapy._private.math_utility._1748 import SquareMatrix
    from mastapy._private.math_utility._1749 import StressPoint
    from mastapy._private.math_utility._1750 import TranslationRotation
    from mastapy._private.math_utility._1751 import Vector2DListAccessor
    from mastapy._private.math_utility._1752 import Vector6D
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility._1702": ["AcousticWeighting"],
        "_private.math_utility._1703": ["AlignmentAxis"],
        "_private.math_utility._1704": ["Axis"],
        "_private.math_utility._1705": ["CirclesOnAxis"],
        "_private.math_utility._1706": ["ComplexMatrix"],
        "_private.math_utility._1707": ["ComplexPartDisplayOption"],
        "_private.math_utility._1708": ["ComplexVector"],
        "_private.math_utility._1709": ["ComplexVector3D"],
        "_private.math_utility._1710": ["ComplexVector6D"],
        "_private.math_utility._1711": ["CoordinateSystem3D"],
        "_private.math_utility._1712": ["CoordinateSystemEditor"],
        "_private.math_utility._1713": ["CoordinateSystemForRotation"],
        "_private.math_utility._1714": ["CoordinateSystemForRotationOrigin"],
        "_private.math_utility._1715": ["DataPrecision"],
        "_private.math_utility._1716": ["DegreeOfFreedom"],
        "_private.math_utility._1717": ["DynamicsResponseScalarResult"],
        "_private.math_utility._1718": ["DynamicsResponseScaling"],
        "_private.math_utility._1719": ["EdgeNamedSelectionDetails"],
        "_private.math_utility._1720": ["Eigenmode"],
        "_private.math_utility._1721": ["Eigenmodes"],
        "_private.math_utility._1722": ["EulerParameters"],
        "_private.math_utility._1723": ["ExtrapolationOptions"],
        "_private.math_utility._1724": ["FacetedBody"],
        "_private.math_utility._1725": ["FacetedSurface"],
        "_private.math_utility._1726": ["FourierSeries"],
        "_private.math_utility._1727": ["GenericMatrix"],
        "_private.math_utility._1728": ["GriddedSurface"],
        "_private.math_utility._1729": ["HarmonicValue"],
        "_private.math_utility._1730": ["InertiaTensor"],
        "_private.math_utility._1731": ["MassProperties"],
        "_private.math_utility._1732": ["MaxMinMean"],
        "_private.math_utility._1733": ["ComplexMagnitudeMethod"],
        "_private.math_utility._1734": ["MultipleFourierSeriesInterpolator"],
        "_private.math_utility._1735": ["Named2DLocation"],
        "_private.math_utility._1736": ["NamedSelection"],
        "_private.math_utility._1737": ["NamedSelectionEdge"],
        "_private.math_utility._1738": ["NamedSelectionFace"],
        "_private.math_utility._1739": ["NamedSelections"],
        "_private.math_utility._1740": ["PIDControlUpdateMethod"],
        "_private.math_utility._1741": ["Quaternion"],
        "_private.math_utility._1742": ["RealMatrix"],
        "_private.math_utility._1743": ["RealVector"],
        "_private.math_utility._1744": ["ResultOptionsFor3DVector"],
        "_private.math_utility._1745": ["RotationAxis"],
        "_private.math_utility._1746": ["RoundedOrder"],
        "_private.math_utility._1747": ["SinCurve"],
        "_private.math_utility._1748": ["SquareMatrix"],
        "_private.math_utility._1749": ["StressPoint"],
        "_private.math_utility._1750": ["TranslationRotation"],
        "_private.math_utility._1751": ["Vector2DListAccessor"],
        "_private.math_utility._1752": ["Vector6D"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticWeighting",
    "AlignmentAxis",
    "Axis",
    "CirclesOnAxis",
    "ComplexMatrix",
    "ComplexPartDisplayOption",
    "ComplexVector",
    "ComplexVector3D",
    "ComplexVector6D",
    "CoordinateSystem3D",
    "CoordinateSystemEditor",
    "CoordinateSystemForRotation",
    "CoordinateSystemForRotationOrigin",
    "DataPrecision",
    "DegreeOfFreedom",
    "DynamicsResponseScalarResult",
    "DynamicsResponseScaling",
    "EdgeNamedSelectionDetails",
    "Eigenmode",
    "Eigenmodes",
    "EulerParameters",
    "ExtrapolationOptions",
    "FacetedBody",
    "FacetedSurface",
    "FourierSeries",
    "GenericMatrix",
    "GriddedSurface",
    "HarmonicValue",
    "InertiaTensor",
    "MassProperties",
    "MaxMinMean",
    "ComplexMagnitudeMethod",
    "MultipleFourierSeriesInterpolator",
    "Named2DLocation",
    "NamedSelection",
    "NamedSelectionEdge",
    "NamedSelectionFace",
    "NamedSelections",
    "PIDControlUpdateMethod",
    "Quaternion",
    "RealMatrix",
    "RealVector",
    "ResultOptionsFor3DVector",
    "RotationAxis",
    "RoundedOrder",
    "SinCurve",
    "SquareMatrix",
    "StressPoint",
    "TranslationRotation",
    "Vector2DListAccessor",
    "Vector6D",
)
