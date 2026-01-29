"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.modal_analysis.gears._2027 import GearMeshForTE
    from mastapy._private.utility.modal_analysis.gears._2028 import GearOrderForTE
    from mastapy._private.utility.modal_analysis.gears._2029 import GearPositions
    from mastapy._private.utility.modal_analysis.gears._2030 import HarmonicOrderForTE
    from mastapy._private.utility.modal_analysis.gears._2031 import LabelOnlyOrder
    from mastapy._private.utility.modal_analysis.gears._2032 import OrderForTE
    from mastapy._private.utility.modal_analysis.gears._2033 import OrderSelector
    from mastapy._private.utility.modal_analysis.gears._2034 import OrderWithRadius
    from mastapy._private.utility.modal_analysis.gears._2035 import RollingBearingOrder
    from mastapy._private.utility.modal_analysis.gears._2036 import ShaftOrderForTE
    from mastapy._private.utility.modal_analysis.gears._2037 import (
        UserDefinedOrderForTE,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.modal_analysis.gears._2027": ["GearMeshForTE"],
        "_private.utility.modal_analysis.gears._2028": ["GearOrderForTE"],
        "_private.utility.modal_analysis.gears._2029": ["GearPositions"],
        "_private.utility.modal_analysis.gears._2030": ["HarmonicOrderForTE"],
        "_private.utility.modal_analysis.gears._2031": ["LabelOnlyOrder"],
        "_private.utility.modal_analysis.gears._2032": ["OrderForTE"],
        "_private.utility.modal_analysis.gears._2033": ["OrderSelector"],
        "_private.utility.modal_analysis.gears._2034": ["OrderWithRadius"],
        "_private.utility.modal_analysis.gears._2035": ["RollingBearingOrder"],
        "_private.utility.modal_analysis.gears._2036": ["ShaftOrderForTE"],
        "_private.utility.modal_analysis.gears._2037": ["UserDefinedOrderForTE"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearMeshForTE",
    "GearOrderForTE",
    "GearPositions",
    "HarmonicOrderForTE",
    "LabelOnlyOrder",
    "OrderForTE",
    "OrderSelector",
    "OrderWithRadius",
    "RollingBearingOrder",
    "ShaftOrderForTE",
    "UserDefinedOrderForTE",
)
