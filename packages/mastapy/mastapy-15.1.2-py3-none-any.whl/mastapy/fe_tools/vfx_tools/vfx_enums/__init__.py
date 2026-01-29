"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.fe_tools.vfx_tools.vfx_enums._1387 import ProSolveEigenmethod
    from mastapy._private.fe_tools.vfx_tools.vfx_enums._1388 import ProSolveMpcType
    from mastapy._private.fe_tools.vfx_tools.vfx_enums._1389 import ProSolveSolverType
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.fe_tools.vfx_tools.vfx_enums._1387": ["ProSolveEigenmethod"],
        "_private.fe_tools.vfx_tools.vfx_enums._1388": ["ProSolveMpcType"],
        "_private.fe_tools.vfx_tools.vfx_enums._1389": ["ProSolveSolverType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ProSolveEigenmethod",
    "ProSolveMpcType",
    "ProSolveSolverType",
)
