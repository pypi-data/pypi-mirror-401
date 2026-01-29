"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1524 import (
        CoolingLoadCaseSettings,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1525 import (
        HeatDissipationReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1526 import (
        HeatFlowReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1527 import (
        HeatTransferCoefficientReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1528 import (
        PowerLosses,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1529 import (
        PressureDropReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1530 import (
        ThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1531 import (
        ThermalLoadCase,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1532 import (
        ThermalLoadCaseGroup,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal.load_cases_and_analyses._1524": [
            "CoolingLoadCaseSettings"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1525": [
            "HeatDissipationReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1526": [
            "HeatFlowReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1527": [
            "HeatTransferCoefficientReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1528": [
            "PowerLosses"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1529": [
            "PressureDropReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1530": [
            "ThermalAnalysis"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1531": [
            "ThermalLoadCase"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1532": [
            "ThermalLoadCaseGroup"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CoolingLoadCaseSettings",
    "HeatDissipationReporter",
    "HeatFlowReporter",
    "HeatTransferCoefficientReporter",
    "PowerLosses",
    "PressureDropReporter",
    "ThermalAnalysis",
    "ThermalLoadCase",
    "ThermalLoadCaseGroup",
)
