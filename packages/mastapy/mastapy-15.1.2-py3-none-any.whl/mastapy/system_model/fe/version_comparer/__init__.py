"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.version_comparer._2681 import DesignResults
    from mastapy._private.system_model.fe.version_comparer._2682 import (
        FESubstructureResults,
    )
    from mastapy._private.system_model.fe.version_comparer._2683 import (
        FESubstructureVersionComparer,
    )
    from mastapy._private.system_model.fe.version_comparer._2684 import LoadCaseResults
    from mastapy._private.system_model.fe.version_comparer._2685 import LoadCasesToRun
    from mastapy._private.system_model.fe.version_comparer._2686 import (
        NodeComparisonResult,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.version_comparer._2681": ["DesignResults"],
        "_private.system_model.fe.version_comparer._2682": ["FESubstructureResults"],
        "_private.system_model.fe.version_comparer._2683": [
            "FESubstructureVersionComparer"
        ],
        "_private.system_model.fe.version_comparer._2684": ["LoadCaseResults"],
        "_private.system_model.fe.version_comparer._2685": ["LoadCasesToRun"],
        "_private.system_model.fe.version_comparer._2686": ["NodeComparisonResult"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DesignResults",
    "FESubstructureResults",
    "FESubstructureVersionComparer",
    "LoadCaseResults",
    "LoadCasesToRun",
    "NodeComparisonResult",
)
