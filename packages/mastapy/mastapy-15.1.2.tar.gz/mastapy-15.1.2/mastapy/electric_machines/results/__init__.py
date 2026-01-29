"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.results._1533 import DynamicForceResults
    from mastapy._private.electric_machines.results._1534 import EfficiencyResults
    from mastapy._private.electric_machines.results._1535 import ElectricMachineDQModel
    from mastapy._private.electric_machines.results._1536 import (
        ElectricMachineMechanicalResults,
    )
    from mastapy._private.electric_machines.results._1537 import (
        ElectricMachineMechanicalResultsViewable,
    )
    from mastapy._private.electric_machines.results._1538 import ElectricMachineResults
    from mastapy._private.electric_machines.results._1539 import (
        ElectricMachineResultsForConductorTurn,
    )
    from mastapy._private.electric_machines.results._1540 import (
        ElectricMachineResultsForConductorTurnAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1541 import (
        ElectricMachineResultsForLineToLine,
    )
    from mastapy._private.electric_machines.results._1542 import (
        ElectricMachineResultsForOpenCircuitAndOnLoad,
    )
    from mastapy._private.electric_machines.results._1543 import (
        ElectricMachineResultsForPhase,
    )
    from mastapy._private.electric_machines.results._1544 import (
        ElectricMachineResultsForPhaseAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1545 import (
        ElectricMachineResultsForStatorToothAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1546 import (
        ElectricMachineResultsLineToLineAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1547 import (
        ElectricMachineResultsTimeStep,
    )
    from mastapy._private.electric_machines.results._1548 import (
        ElectricMachineResultsTimeStepAtLocation,
    )
    from mastapy._private.electric_machines.results._1549 import (
        ElectricMachineResultsViewable,
    )
    from mastapy._private.electric_machines.results._1550 import (
        ElectricMachineForceViewOptions,
    )
    from mastapy._private.electric_machines.results._1552 import LinearDQModel
    from mastapy._private.electric_machines.results._1553 import (
        MaximumTorqueResultsPoints,
    )
    from mastapy._private.electric_machines.results._1554 import NonLinearDQModel
    from mastapy._private.electric_machines.results._1555 import (
        NonLinearDQModelGeneratorSettings,
    )
    from mastapy._private.electric_machines.results._1556 import (
        OnLoadElectricMachineResults,
    )
    from mastapy._private.electric_machines.results._1557 import (
        OpenCircuitElectricMachineResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.results._1533": ["DynamicForceResults"],
        "_private.electric_machines.results._1534": ["EfficiencyResults"],
        "_private.electric_machines.results._1535": ["ElectricMachineDQModel"],
        "_private.electric_machines.results._1536": [
            "ElectricMachineMechanicalResults"
        ],
        "_private.electric_machines.results._1537": [
            "ElectricMachineMechanicalResultsViewable"
        ],
        "_private.electric_machines.results._1538": ["ElectricMachineResults"],
        "_private.electric_machines.results._1539": [
            "ElectricMachineResultsForConductorTurn"
        ],
        "_private.electric_machines.results._1540": [
            "ElectricMachineResultsForConductorTurnAtTimeStep"
        ],
        "_private.electric_machines.results._1541": [
            "ElectricMachineResultsForLineToLine"
        ],
        "_private.electric_machines.results._1542": [
            "ElectricMachineResultsForOpenCircuitAndOnLoad"
        ],
        "_private.electric_machines.results._1543": ["ElectricMachineResultsForPhase"],
        "_private.electric_machines.results._1544": [
            "ElectricMachineResultsForPhaseAtTimeStep"
        ],
        "_private.electric_machines.results._1545": [
            "ElectricMachineResultsForStatorToothAtTimeStep"
        ],
        "_private.electric_machines.results._1546": [
            "ElectricMachineResultsLineToLineAtTimeStep"
        ],
        "_private.electric_machines.results._1547": ["ElectricMachineResultsTimeStep"],
        "_private.electric_machines.results._1548": [
            "ElectricMachineResultsTimeStepAtLocation"
        ],
        "_private.electric_machines.results._1549": ["ElectricMachineResultsViewable"],
        "_private.electric_machines.results._1550": ["ElectricMachineForceViewOptions"],
        "_private.electric_machines.results._1552": ["LinearDQModel"],
        "_private.electric_machines.results._1553": ["MaximumTorqueResultsPoints"],
        "_private.electric_machines.results._1554": ["NonLinearDQModel"],
        "_private.electric_machines.results._1555": [
            "NonLinearDQModelGeneratorSettings"
        ],
        "_private.electric_machines.results._1556": ["OnLoadElectricMachineResults"],
        "_private.electric_machines.results._1557": [
            "OpenCircuitElectricMachineResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DynamicForceResults",
    "EfficiencyResults",
    "ElectricMachineDQModel",
    "ElectricMachineMechanicalResults",
    "ElectricMachineMechanicalResultsViewable",
    "ElectricMachineResults",
    "ElectricMachineResultsForConductorTurn",
    "ElectricMachineResultsForConductorTurnAtTimeStep",
    "ElectricMachineResultsForLineToLine",
    "ElectricMachineResultsForOpenCircuitAndOnLoad",
    "ElectricMachineResultsForPhase",
    "ElectricMachineResultsForPhaseAtTimeStep",
    "ElectricMachineResultsForStatorToothAtTimeStep",
    "ElectricMachineResultsLineToLineAtTimeStep",
    "ElectricMachineResultsTimeStep",
    "ElectricMachineResultsTimeStepAtLocation",
    "ElectricMachineResultsViewable",
    "ElectricMachineForceViewOptions",
    "LinearDQModel",
    "MaximumTorqueResultsPoints",
    "NonLinearDQModel",
    "NonLinearDQModelGeneratorSettings",
    "OnLoadElectricMachineResults",
    "OpenCircuitElectricMachineResults",
)
