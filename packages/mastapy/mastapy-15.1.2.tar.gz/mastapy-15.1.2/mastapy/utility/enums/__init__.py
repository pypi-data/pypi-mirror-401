"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.enums._2049 import BearingForceArrowOption
    from mastapy._private.utility.enums._2050 import PropertySpecificationMethod
    from mastapy._private.utility.enums._2051 import SplineForceArrowOption
    from mastapy._private.utility.enums._2052 import TableAndChartOptions
    from mastapy._private.utility.enums._2053 import ThreeDViewContourOption
    from mastapy._private.utility.enums._2054 import (
        ThreeDViewContourOptionFirstSelection,
    )
    from mastapy._private.utility.enums._2055 import (
        ThreeDViewContourOptionSecondSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.enums._2049": ["BearingForceArrowOption"],
        "_private.utility.enums._2050": ["PropertySpecificationMethod"],
        "_private.utility.enums._2051": ["SplineForceArrowOption"],
        "_private.utility.enums._2052": ["TableAndChartOptions"],
        "_private.utility.enums._2053": ["ThreeDViewContourOption"],
        "_private.utility.enums._2054": ["ThreeDViewContourOptionFirstSelection"],
        "_private.utility.enums._2055": ["ThreeDViewContourOptionSecondSelection"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingForceArrowOption",
    "PropertySpecificationMethod",
    "SplineForceArrowOption",
    "TableAndChartOptions",
    "ThreeDViewContourOption",
    "ThreeDViewContourOptionFirstSelection",
    "ThreeDViewContourOptionSecondSelection",
)
