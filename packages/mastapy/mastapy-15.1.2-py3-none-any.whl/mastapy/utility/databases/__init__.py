"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.databases._2056 import ConnectionState
    from mastapy._private.utility.databases._2057 import Database
    from mastapy._private.utility.databases._2058 import DatabaseConnectionSettings
    from mastapy._private.utility.databases._2059 import DatabaseKey
    from mastapy._private.utility.databases._2060 import DatabaseSettings
    from mastapy._private.utility.databases._2061 import NamedDatabase
    from mastapy._private.utility.databases._2062 import NamedDatabaseItem
    from mastapy._private.utility.databases._2063 import NamedKey
    from mastapy._private.utility.databases._2064 import (
        NetworkDatabaseConnectionSettingsItem,
    )
    from mastapy._private.utility.databases._2065 import SQLDatabase
    from mastapy._private.utility.databases._2066 import VersionUpdater
    from mastapy._private.utility.databases._2067 import VersionUpdaterSelectableItem
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.databases._2056": ["ConnectionState"],
        "_private.utility.databases._2057": ["Database"],
        "_private.utility.databases._2058": ["DatabaseConnectionSettings"],
        "_private.utility.databases._2059": ["DatabaseKey"],
        "_private.utility.databases._2060": ["DatabaseSettings"],
        "_private.utility.databases._2061": ["NamedDatabase"],
        "_private.utility.databases._2062": ["NamedDatabaseItem"],
        "_private.utility.databases._2063": ["NamedKey"],
        "_private.utility.databases._2064": ["NetworkDatabaseConnectionSettingsItem"],
        "_private.utility.databases._2065": ["SQLDatabase"],
        "_private.utility.databases._2066": ["VersionUpdater"],
        "_private.utility.databases._2067": ["VersionUpdaterSelectableItem"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConnectionState",
    "Database",
    "DatabaseConnectionSettings",
    "DatabaseKey",
    "DatabaseSettings",
    "NamedDatabase",
    "NamedDatabaseItem",
    "NamedKey",
    "NetworkDatabaseConnectionSettingsItem",
    "SQLDatabase",
    "VersionUpdater",
    "VersionUpdaterSelectableItem",
)
