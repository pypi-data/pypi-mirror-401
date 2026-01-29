"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7960 import ApiEnumForAttribute
    from mastapy._private.scripting._7961 import ApiVersion
    from mastapy._private.scripting._7962 import SMTBitmap
    from mastapy._private.scripting._7964 import MastaPropertyAttribute
    from mastapy._private.scripting._7965 import PythonCommand
    from mastapy._private.scripting._7966 import ScriptingCommand
    from mastapy._private.scripting._7967 import ScriptingExecutionCommand
    from mastapy._private.scripting._7968 import ScriptingObjectCommand
    from mastapy._private.scripting._7969 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7960": ["ApiEnumForAttribute"],
        "_private.scripting._7961": ["ApiVersion"],
        "_private.scripting._7962": ["SMTBitmap"],
        "_private.scripting._7964": ["MastaPropertyAttribute"],
        "_private.scripting._7965": ["PythonCommand"],
        "_private.scripting._7966": ["ScriptingCommand"],
        "_private.scripting._7967": ["ScriptingExecutionCommand"],
        "_private.scripting._7968": ["ScriptingObjectCommand"],
        "_private.scripting._7969": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
