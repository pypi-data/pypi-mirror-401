"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines._1392 import AbstractStator
    from mastapy._private.electric_machines._1393 import AbstractToothAndSlot
    from mastapy._private.electric_machines._1394 import CADConductor
    from mastapy._private.electric_machines._1395 import CADElectricMachineDetail
    from mastapy._private.electric_machines._1396 import CADFieldWindingSpecification
    from mastapy._private.electric_machines._1397 import CADMagnetDetails
    from mastapy._private.electric_machines._1398 import CADMagnetsForLayer
    from mastapy._private.electric_machines._1399 import CADRotor
    from mastapy._private.electric_machines._1400 import CADStator
    from mastapy._private.electric_machines._1401 import CADToothAndSlot
    from mastapy._private.electric_machines._1402 import CADWoundFieldSynchronousRotor
    from mastapy._private.electric_machines._1403 import Coil
    from mastapy._private.electric_machines._1404 import CoilPositionInSlot
    from mastapy._private.electric_machines._1405 import CoolingChannelShape
    from mastapy._private.electric_machines._1406 import CoolingDuctLayerSpecification
    from mastapy._private.electric_machines._1407 import CoolingDuctShape
    from mastapy._private.electric_machines._1408 import (
        CoreLossBuildFactorSpecificationMethod,
    )
    from mastapy._private.electric_machines._1409 import CoreLossCoefficients
    from mastapy._private.electric_machines._1410 import DoubleLayerWindingSlotPositions
    from mastapy._private.electric_machines._1411 import DQAxisConvention
    from mastapy._private.electric_machines._1412 import Eccentricity
    from mastapy._private.electric_machines._1413 import ElectricMachineDesignBase
    from mastapy._private.electric_machines._1414 import ElectricMachineDetail
    from mastapy._private.electric_machines._1415 import (
        ElectricMachineDetailInitialInformation,
    )
    from mastapy._private.electric_machines._1416 import (
        ElectricMachineElectromagneticAndThermalMeshingOptions,
    )
    from mastapy._private.electric_machines._1417 import ElectricMachineGroup
    from mastapy._private.electric_machines._1418 import (
        ElectricMachineMechanicalAnalysisMeshingOptions,
    )
    from mastapy._private.electric_machines._1419 import ElectricMachineMeshingOptions
    from mastapy._private.electric_machines._1420 import (
        ElectricMachineMeshingOptionsBase,
    )
    from mastapy._private.electric_machines._1421 import ElectricMachineSetup
    from mastapy._private.electric_machines._1422 import ElectricMachineSetupBase
    from mastapy._private.electric_machines._1423 import (
        ElectricMachineThermalMeshingOptions,
    )
    from mastapy._private.electric_machines._1424 import ElectricMachineType
    from mastapy._private.electric_machines._1425 import FieldWindingSpecification
    from mastapy._private.electric_machines._1426 import FieldWindingSpecificationBase
    from mastapy._private.electric_machines._1427 import FillFactorSpecificationMethod
    from mastapy._private.electric_machines._1428 import FluxBarriers
    from mastapy._private.electric_machines._1429 import FluxBarrierOrWeb
    from mastapy._private.electric_machines._1430 import FluxBarrierStyle
    from mastapy._private.electric_machines._1431 import GeneralElectricMachineMaterial
    from mastapy._private.electric_machines._1432 import (
        GeneralElectricMachineMaterialDatabase,
    )
    from mastapy._private.electric_machines._1433 import HairpinConductor
    from mastapy._private.electric_machines._1434 import (
        HarmonicLoadDataControlExcitationOptionForElectricMachineMode,
    )
    from mastapy._private.electric_machines._1435 import (
        IndividualConductorSpecificationSource,
    )
    from mastapy._private.electric_machines._1436 import (
        InteriorPermanentMagnetAndSynchronousReluctanceRotor,
    )
    from mastapy._private.electric_machines._1437 import InteriorPermanentMagnetMachine
    from mastapy._private.electric_machines._1438 import (
        IronLossCoefficientSpecificationMethod,
    )
    from mastapy._private.electric_machines._1439 import MagnetClearance
    from mastapy._private.electric_machines._1440 import MagnetConfiguration
    from mastapy._private.electric_machines._1441 import MagnetData
    from mastapy._private.electric_machines._1442 import MagnetDesign
    from mastapy._private.electric_machines._1443 import MagnetForLayer
    from mastapy._private.electric_machines._1444 import MagnetisationDirection
    from mastapy._private.electric_machines._1445 import MagnetMaterial
    from mastapy._private.electric_machines._1446 import MagnetMaterialDatabase
    from mastapy._private.electric_machines._1447 import MotorRotorSideFaceDetail
    from mastapy._private.electric_machines._1448 import NonCADElectricMachineDetail
    from mastapy._private.electric_machines._1449 import NotchShape
    from mastapy._private.electric_machines._1450 import NotchSpecification
    from mastapy._private.electric_machines._1451 import (
        PermanentMagnetAssistedSynchronousReluctanceMachine,
    )
    from mastapy._private.electric_machines._1452 import PermanentMagnetRotor
    from mastapy._private.electric_machines._1453 import Phase
    from mastapy._private.electric_machines._1454 import RegionID
    from mastapy._private.electric_machines._1455 import RemanenceModifier
    from mastapy._private.electric_machines._1456 import ResultsLocationsSpecification
    from mastapy._private.electric_machines._1457 import Rotor
    from mastapy._private.electric_machines._1458 import RotorInternalLayerSpecification
    from mastapy._private.electric_machines._1459 import RotorSkewSlice
    from mastapy._private.electric_machines._1460 import RotorType
    from mastapy._private.electric_machines._1461 import SingleOrDoubleLayerWindings
    from mastapy._private.electric_machines._1462 import SlotSectionDetail
    from mastapy._private.electric_machines._1463 import Stator
    from mastapy._private.electric_machines._1464 import StatorCutoutSpecification
    from mastapy._private.electric_machines._1465 import StatorRotorMaterial
    from mastapy._private.electric_machines._1466 import StatorRotorMaterialDatabase
    from mastapy._private.electric_machines._1467 import SurfacePermanentMagnetMachine
    from mastapy._private.electric_machines._1468 import SurfacePermanentMagnetRotor
    from mastapy._private.electric_machines._1469 import SynchronousReluctanceMachine
    from mastapy._private.electric_machines._1470 import ToothAndSlot
    from mastapy._private.electric_machines._1471 import ToothSlotStyle
    from mastapy._private.electric_machines._1472 import ToothTaperSpecification
    from mastapy._private.electric_machines._1473 import (
        TwoDimensionalFEModelForAnalysis,
    )
    from mastapy._private.electric_machines._1474 import (
        TwoDimensionalFEModelForElectromagneticAnalysis,
    )
    from mastapy._private.electric_machines._1475 import (
        TwoDimensionalFEModelForMechanicalAnalysis,
    )
    from mastapy._private.electric_machines._1476 import UShapedLayerSpecification
    from mastapy._private.electric_machines._1477 import VShapedMagnetLayerSpecification
    from mastapy._private.electric_machines._1478 import WindingConductor
    from mastapy._private.electric_machines._1479 import WindingConnection
    from mastapy._private.electric_machines._1480 import WindingMaterial
    from mastapy._private.electric_machines._1481 import WindingMaterialDatabase
    from mastapy._private.electric_machines._1482 import Windings
    from mastapy._private.electric_machines._1483 import WindingsViewer
    from mastapy._private.electric_machines._1484 import WindingType
    from mastapy._private.electric_machines._1485 import WireSizeSpecificationMethod
    from mastapy._private.electric_machines._1486 import WoundFieldSynchronousMachine
    from mastapy._private.electric_machines._1487 import WoundFieldSynchronousRotor
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines._1392": ["AbstractStator"],
        "_private.electric_machines._1393": ["AbstractToothAndSlot"],
        "_private.electric_machines._1394": ["CADConductor"],
        "_private.electric_machines._1395": ["CADElectricMachineDetail"],
        "_private.electric_machines._1396": ["CADFieldWindingSpecification"],
        "_private.electric_machines._1397": ["CADMagnetDetails"],
        "_private.electric_machines._1398": ["CADMagnetsForLayer"],
        "_private.electric_machines._1399": ["CADRotor"],
        "_private.electric_machines._1400": ["CADStator"],
        "_private.electric_machines._1401": ["CADToothAndSlot"],
        "_private.electric_machines._1402": ["CADWoundFieldSynchronousRotor"],
        "_private.electric_machines._1403": ["Coil"],
        "_private.electric_machines._1404": ["CoilPositionInSlot"],
        "_private.electric_machines._1405": ["CoolingChannelShape"],
        "_private.electric_machines._1406": ["CoolingDuctLayerSpecification"],
        "_private.electric_machines._1407": ["CoolingDuctShape"],
        "_private.electric_machines._1408": ["CoreLossBuildFactorSpecificationMethod"],
        "_private.electric_machines._1409": ["CoreLossCoefficients"],
        "_private.electric_machines._1410": ["DoubleLayerWindingSlotPositions"],
        "_private.electric_machines._1411": ["DQAxisConvention"],
        "_private.electric_machines._1412": ["Eccentricity"],
        "_private.electric_machines._1413": ["ElectricMachineDesignBase"],
        "_private.electric_machines._1414": ["ElectricMachineDetail"],
        "_private.electric_machines._1415": ["ElectricMachineDetailInitialInformation"],
        "_private.electric_machines._1416": [
            "ElectricMachineElectromagneticAndThermalMeshingOptions"
        ],
        "_private.electric_machines._1417": ["ElectricMachineGroup"],
        "_private.electric_machines._1418": [
            "ElectricMachineMechanicalAnalysisMeshingOptions"
        ],
        "_private.electric_machines._1419": ["ElectricMachineMeshingOptions"],
        "_private.electric_machines._1420": ["ElectricMachineMeshingOptionsBase"],
        "_private.electric_machines._1421": ["ElectricMachineSetup"],
        "_private.electric_machines._1422": ["ElectricMachineSetupBase"],
        "_private.electric_machines._1423": ["ElectricMachineThermalMeshingOptions"],
        "_private.electric_machines._1424": ["ElectricMachineType"],
        "_private.electric_machines._1425": ["FieldWindingSpecification"],
        "_private.electric_machines._1426": ["FieldWindingSpecificationBase"],
        "_private.electric_machines._1427": ["FillFactorSpecificationMethod"],
        "_private.electric_machines._1428": ["FluxBarriers"],
        "_private.electric_machines._1429": ["FluxBarrierOrWeb"],
        "_private.electric_machines._1430": ["FluxBarrierStyle"],
        "_private.electric_machines._1431": ["GeneralElectricMachineMaterial"],
        "_private.electric_machines._1432": ["GeneralElectricMachineMaterialDatabase"],
        "_private.electric_machines._1433": ["HairpinConductor"],
        "_private.electric_machines._1434": [
            "HarmonicLoadDataControlExcitationOptionForElectricMachineMode"
        ],
        "_private.electric_machines._1435": ["IndividualConductorSpecificationSource"],
        "_private.electric_machines._1436": [
            "InteriorPermanentMagnetAndSynchronousReluctanceRotor"
        ],
        "_private.electric_machines._1437": ["InteriorPermanentMagnetMachine"],
        "_private.electric_machines._1438": ["IronLossCoefficientSpecificationMethod"],
        "_private.electric_machines._1439": ["MagnetClearance"],
        "_private.electric_machines._1440": ["MagnetConfiguration"],
        "_private.electric_machines._1441": ["MagnetData"],
        "_private.electric_machines._1442": ["MagnetDesign"],
        "_private.electric_machines._1443": ["MagnetForLayer"],
        "_private.electric_machines._1444": ["MagnetisationDirection"],
        "_private.electric_machines._1445": ["MagnetMaterial"],
        "_private.electric_machines._1446": ["MagnetMaterialDatabase"],
        "_private.electric_machines._1447": ["MotorRotorSideFaceDetail"],
        "_private.electric_machines._1448": ["NonCADElectricMachineDetail"],
        "_private.electric_machines._1449": ["NotchShape"],
        "_private.electric_machines._1450": ["NotchSpecification"],
        "_private.electric_machines._1451": [
            "PermanentMagnetAssistedSynchronousReluctanceMachine"
        ],
        "_private.electric_machines._1452": ["PermanentMagnetRotor"],
        "_private.electric_machines._1453": ["Phase"],
        "_private.electric_machines._1454": ["RegionID"],
        "_private.electric_machines._1455": ["RemanenceModifier"],
        "_private.electric_machines._1456": ["ResultsLocationsSpecification"],
        "_private.electric_machines._1457": ["Rotor"],
        "_private.electric_machines._1458": ["RotorInternalLayerSpecification"],
        "_private.electric_machines._1459": ["RotorSkewSlice"],
        "_private.electric_machines._1460": ["RotorType"],
        "_private.electric_machines._1461": ["SingleOrDoubleLayerWindings"],
        "_private.electric_machines._1462": ["SlotSectionDetail"],
        "_private.electric_machines._1463": ["Stator"],
        "_private.electric_machines._1464": ["StatorCutoutSpecification"],
        "_private.electric_machines._1465": ["StatorRotorMaterial"],
        "_private.electric_machines._1466": ["StatorRotorMaterialDatabase"],
        "_private.electric_machines._1467": ["SurfacePermanentMagnetMachine"],
        "_private.electric_machines._1468": ["SurfacePermanentMagnetRotor"],
        "_private.electric_machines._1469": ["SynchronousReluctanceMachine"],
        "_private.electric_machines._1470": ["ToothAndSlot"],
        "_private.electric_machines._1471": ["ToothSlotStyle"],
        "_private.electric_machines._1472": ["ToothTaperSpecification"],
        "_private.electric_machines._1473": ["TwoDimensionalFEModelForAnalysis"],
        "_private.electric_machines._1474": [
            "TwoDimensionalFEModelForElectromagneticAnalysis"
        ],
        "_private.electric_machines._1475": [
            "TwoDimensionalFEModelForMechanicalAnalysis"
        ],
        "_private.electric_machines._1476": ["UShapedLayerSpecification"],
        "_private.electric_machines._1477": ["VShapedMagnetLayerSpecification"],
        "_private.electric_machines._1478": ["WindingConductor"],
        "_private.electric_machines._1479": ["WindingConnection"],
        "_private.electric_machines._1480": ["WindingMaterial"],
        "_private.electric_machines._1481": ["WindingMaterialDatabase"],
        "_private.electric_machines._1482": ["Windings"],
        "_private.electric_machines._1483": ["WindingsViewer"],
        "_private.electric_machines._1484": ["WindingType"],
        "_private.electric_machines._1485": ["WireSizeSpecificationMethod"],
        "_private.electric_machines._1486": ["WoundFieldSynchronousMachine"],
        "_private.electric_machines._1487": ["WoundFieldSynchronousRotor"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStator",
    "AbstractToothAndSlot",
    "CADConductor",
    "CADElectricMachineDetail",
    "CADFieldWindingSpecification",
    "CADMagnetDetails",
    "CADMagnetsForLayer",
    "CADRotor",
    "CADStator",
    "CADToothAndSlot",
    "CADWoundFieldSynchronousRotor",
    "Coil",
    "CoilPositionInSlot",
    "CoolingChannelShape",
    "CoolingDuctLayerSpecification",
    "CoolingDuctShape",
    "CoreLossBuildFactorSpecificationMethod",
    "CoreLossCoefficients",
    "DoubleLayerWindingSlotPositions",
    "DQAxisConvention",
    "Eccentricity",
    "ElectricMachineDesignBase",
    "ElectricMachineDetail",
    "ElectricMachineDetailInitialInformation",
    "ElectricMachineElectromagneticAndThermalMeshingOptions",
    "ElectricMachineGroup",
    "ElectricMachineMechanicalAnalysisMeshingOptions",
    "ElectricMachineMeshingOptions",
    "ElectricMachineMeshingOptionsBase",
    "ElectricMachineSetup",
    "ElectricMachineSetupBase",
    "ElectricMachineThermalMeshingOptions",
    "ElectricMachineType",
    "FieldWindingSpecification",
    "FieldWindingSpecificationBase",
    "FillFactorSpecificationMethod",
    "FluxBarriers",
    "FluxBarrierOrWeb",
    "FluxBarrierStyle",
    "GeneralElectricMachineMaterial",
    "GeneralElectricMachineMaterialDatabase",
    "HairpinConductor",
    "HarmonicLoadDataControlExcitationOptionForElectricMachineMode",
    "IndividualConductorSpecificationSource",
    "InteriorPermanentMagnetAndSynchronousReluctanceRotor",
    "InteriorPermanentMagnetMachine",
    "IronLossCoefficientSpecificationMethod",
    "MagnetClearance",
    "MagnetConfiguration",
    "MagnetData",
    "MagnetDesign",
    "MagnetForLayer",
    "MagnetisationDirection",
    "MagnetMaterial",
    "MagnetMaterialDatabase",
    "MotorRotorSideFaceDetail",
    "NonCADElectricMachineDetail",
    "NotchShape",
    "NotchSpecification",
    "PermanentMagnetAssistedSynchronousReluctanceMachine",
    "PermanentMagnetRotor",
    "Phase",
    "RegionID",
    "RemanenceModifier",
    "ResultsLocationsSpecification",
    "Rotor",
    "RotorInternalLayerSpecification",
    "RotorSkewSlice",
    "RotorType",
    "SingleOrDoubleLayerWindings",
    "SlotSectionDetail",
    "Stator",
    "StatorCutoutSpecification",
    "StatorRotorMaterial",
    "StatorRotorMaterialDatabase",
    "SurfacePermanentMagnetMachine",
    "SurfacePermanentMagnetRotor",
    "SynchronousReluctanceMachine",
    "ToothAndSlot",
    "ToothSlotStyle",
    "ToothTaperSpecification",
    "TwoDimensionalFEModelForAnalysis",
    "TwoDimensionalFEModelForElectromagneticAnalysis",
    "TwoDimensionalFEModelForMechanicalAnalysis",
    "UShapedLayerSpecification",
    "VShapedMagnetLayerSpecification",
    "WindingConductor",
    "WindingConnection",
    "WindingMaterial",
    "WindingMaterialDatabase",
    "Windings",
    "WindingsViewer",
    "WindingType",
    "WireSizeSpecificationMethod",
    "WoundFieldSynchronousMachine",
    "WoundFieldSynchronousRotor",
)
