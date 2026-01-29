"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal._1488 import (
        AdditionalSliceSpecification,
    )
    from mastapy._private.electric_machines.thermal._1489 import Channel
    from mastapy._private.electric_machines.thermal._1490 import ComponentSetup
    from mastapy._private.electric_machines.thermal._1491 import (
        CoolingChannelForThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal._1492 import CoolingJacketType
    from mastapy._private.electric_machines.thermal._1493 import EdgeSelector
    from mastapy._private.electric_machines.thermal._1494 import (
        EndWindingCoolingFlowSource,
    )
    from mastapy._private.electric_machines.thermal._1495 import EndWindingLengthSource
    from mastapy._private.electric_machines.thermal._1496 import (
        EndWindingThermalElement,
    )
    from mastapy._private.electric_machines.thermal._1497 import (
        HeatTransferCoefficientCalculationMethod,
    )
    from mastapy._private.electric_machines.thermal._1498 import (
        HousingChannelModificationFactors,
    )
    from mastapy._private.electric_machines.thermal._1499 import HousingFlowDirection
    from mastapy._private.electric_machines.thermal._1500 import InitialInformation
    from mastapy._private.electric_machines.thermal._1501 import InletLocation
    from mastapy._private.electric_machines.thermal._1502 import (
        RegionIDForThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal._1503 import RotorSetup
    from mastapy._private.electric_machines.thermal._1504 import SliceLengthInformation
    from mastapy._private.electric_machines.thermal._1505 import (
        SliceLengthInformationPerRegion,
    )
    from mastapy._private.electric_machines.thermal._1506 import (
        SliceLengthInformationReporter,
    )
    from mastapy._private.electric_machines.thermal._1507 import StatorSetup
    from mastapy._private.electric_machines.thermal._1508 import ThermalElectricMachine
    from mastapy._private.electric_machines.thermal._1509 import (
        ThermalElectricMachineSetup,
    )
    from mastapy._private.electric_machines.thermal._1510 import ThermalEndcap
    from mastapy._private.electric_machines.thermal._1511 import ThermalEndWinding
    from mastapy._private.electric_machines.thermal._1512 import (
        ThermalEndWindingSurfaceCollection,
    )
    from mastapy._private.electric_machines.thermal._1513 import ThermalHousing
    from mastapy._private.electric_machines.thermal._1514 import ThermalRotor
    from mastapy._private.electric_machines.thermal._1515 import ThermalStator
    from mastapy._private.electric_machines.thermal._1516 import ThermalWindings
    from mastapy._private.electric_machines.thermal._1517 import (
        UserSpecifiedEdgeIndices,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal._1488": ["AdditionalSliceSpecification"],
        "_private.electric_machines.thermal._1489": ["Channel"],
        "_private.electric_machines.thermal._1490": ["ComponentSetup"],
        "_private.electric_machines.thermal._1491": [
            "CoolingChannelForThermalAnalysis"
        ],
        "_private.electric_machines.thermal._1492": ["CoolingJacketType"],
        "_private.electric_machines.thermal._1493": ["EdgeSelector"],
        "_private.electric_machines.thermal._1494": ["EndWindingCoolingFlowSource"],
        "_private.electric_machines.thermal._1495": ["EndWindingLengthSource"],
        "_private.electric_machines.thermal._1496": ["EndWindingThermalElement"],
        "_private.electric_machines.thermal._1497": [
            "HeatTransferCoefficientCalculationMethod"
        ],
        "_private.electric_machines.thermal._1498": [
            "HousingChannelModificationFactors"
        ],
        "_private.electric_machines.thermal._1499": ["HousingFlowDirection"],
        "_private.electric_machines.thermal._1500": ["InitialInformation"],
        "_private.electric_machines.thermal._1501": ["InletLocation"],
        "_private.electric_machines.thermal._1502": ["RegionIDForThermalAnalysis"],
        "_private.electric_machines.thermal._1503": ["RotorSetup"],
        "_private.electric_machines.thermal._1504": ["SliceLengthInformation"],
        "_private.electric_machines.thermal._1505": ["SliceLengthInformationPerRegion"],
        "_private.electric_machines.thermal._1506": ["SliceLengthInformationReporter"],
        "_private.electric_machines.thermal._1507": ["StatorSetup"],
        "_private.electric_machines.thermal._1508": ["ThermalElectricMachine"],
        "_private.electric_machines.thermal._1509": ["ThermalElectricMachineSetup"],
        "_private.electric_machines.thermal._1510": ["ThermalEndcap"],
        "_private.electric_machines.thermal._1511": ["ThermalEndWinding"],
        "_private.electric_machines.thermal._1512": [
            "ThermalEndWindingSurfaceCollection"
        ],
        "_private.electric_machines.thermal._1513": ["ThermalHousing"],
        "_private.electric_machines.thermal._1514": ["ThermalRotor"],
        "_private.electric_machines.thermal._1515": ["ThermalStator"],
        "_private.electric_machines.thermal._1516": ["ThermalWindings"],
        "_private.electric_machines.thermal._1517": ["UserSpecifiedEdgeIndices"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdditionalSliceSpecification",
    "Channel",
    "ComponentSetup",
    "CoolingChannelForThermalAnalysis",
    "CoolingJacketType",
    "EdgeSelector",
    "EndWindingCoolingFlowSource",
    "EndWindingLengthSource",
    "EndWindingThermalElement",
    "HeatTransferCoefficientCalculationMethod",
    "HousingChannelModificationFactors",
    "HousingFlowDirection",
    "InitialInformation",
    "InletLocation",
    "RegionIDForThermalAnalysis",
    "RotorSetup",
    "SliceLengthInformation",
    "SliceLengthInformationPerRegion",
    "SliceLengthInformationReporter",
    "StatorSetup",
    "ThermalElectricMachine",
    "ThermalElectricMachineSetup",
    "ThermalEndcap",
    "ThermalEndWinding",
    "ThermalEndWindingSurfaceCollection",
    "ThermalHousing",
    "ThermalRotor",
    "ThermalStator",
    "ThermalWindings",
    "UserSpecifiedEdgeIndices",
)
