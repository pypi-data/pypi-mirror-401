"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal.results._1518 import (
        ThermalResultAtLocation,
    )
    from mastapy._private.electric_machines.thermal.results._1519 import ThermalResults
    from mastapy._private.electric_machines.thermal.results._1520 import (
        ThermalResultsForFEComponent,
    )
    from mastapy._private.electric_machines.thermal.results._1521 import (
        ThermalResultsForFERegionOrBoundary,
    )
    from mastapy._private.electric_machines.thermal.results._1522 import (
        ThermalResultsForFESlice,
    )
    from mastapy._private.electric_machines.thermal.results._1523 import (
        ThermalResultsForLPTNNode,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal.results._1518": ["ThermalResultAtLocation"],
        "_private.electric_machines.thermal.results._1519": ["ThermalResults"],
        "_private.electric_machines.thermal.results._1520": [
            "ThermalResultsForFEComponent"
        ],
        "_private.electric_machines.thermal.results._1521": [
            "ThermalResultsForFERegionOrBoundary"
        ],
        "_private.electric_machines.thermal.results._1522": [
            "ThermalResultsForFESlice"
        ],
        "_private.electric_machines.thermal.results._1523": [
            "ThermalResultsForLPTNNode"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ThermalResultAtLocation",
    "ThermalResults",
    "ThermalResultsForFEComponent",
    "ThermalResultsForFERegionOrBoundary",
    "ThermalResultsForFESlice",
    "ThermalResultsForLPTNNode",
)
