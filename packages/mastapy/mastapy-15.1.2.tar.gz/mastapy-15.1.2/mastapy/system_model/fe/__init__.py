"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe._2615 import AlignConnectedComponentOptions
    from mastapy._private.system_model.fe._2616 import AlignmentMethod
    from mastapy._private.system_model.fe._2617 import AlignmentMethodForRaceBearing
    from mastapy._private.system_model.fe._2618 import AlignmentUsingAxialNodePositions
    from mastapy._private.system_model.fe._2619 import AngleSource
    from mastapy._private.system_model.fe._2620 import BaseFEWithSelection
    from mastapy._private.system_model.fe._2621 import BatchOperations
    from mastapy._private.system_model.fe._2622 import BearingNodeAlignmentOption
    from mastapy._private.system_model.fe._2623 import BearingNodeOption
    from mastapy._private.system_model.fe._2624 import BearingRaceNodeLink
    from mastapy._private.system_model.fe._2625 import BearingRacePosition
    from mastapy._private.system_model.fe._2626 import ComponentOrientationOption
    from mastapy._private.system_model.fe._2627 import ContactPairWithSelection
    from mastapy._private.system_model.fe._2628 import CoordinateSystemWithSelection
    from mastapy._private.system_model.fe._2629 import CreateConnectedComponentOptions
    from mastapy._private.system_model.fe._2630 import (
        CreateMicrophoneNormalToSurfaceOptions,
    )
    from mastapy._private.system_model.fe._2631 import DegreeOfFreedomBoundaryCondition
    from mastapy._private.system_model.fe._2632 import (
        DegreeOfFreedomBoundaryConditionAngular,
    )
    from mastapy._private.system_model.fe._2633 import (
        DegreeOfFreedomBoundaryConditionLinear,
    )
    from mastapy._private.system_model.fe._2634 import ElectricMachineDataSet
    from mastapy._private.system_model.fe._2635 import ElectricMachineDynamicLoadData
    from mastapy._private.system_model.fe._2636 import ElementFaceGroupWithSelection
    from mastapy._private.system_model.fe._2637 import ElementPropertiesWithSelection
    from mastapy._private.system_model.fe._2638 import ExportOptionsForNode
    from mastapy._private.system_model.fe._2639 import (
        ExportOptionsForNodeWithBoundaryConditionType,
    )
    from mastapy._private.system_model.fe._2640 import FEEntityGroupWithSelection
    from mastapy._private.system_model.fe._2641 import FEExportSettings
    from mastapy._private.system_model.fe._2642 import FEPartDRIVASurfaceSelection
    from mastapy._private.system_model.fe._2643 import FEPartWithBatchOptions
    from mastapy._private.system_model.fe._2644 import FEStiffnessGeometry
    from mastapy._private.system_model.fe._2645 import FEStiffnessTester
    from mastapy._private.system_model.fe._2646 import FESubstructure
    from mastapy._private.system_model.fe._2647 import FESubstructureExportOptions
    from mastapy._private.system_model.fe._2648 import FESubstructureNode
    from mastapy._private.system_model.fe._2649 import FESubstructureNodeModeShape
    from mastapy._private.system_model.fe._2650 import FESubstructureNodeModeShapes
    from mastapy._private.system_model.fe._2651 import FESubstructureType
    from mastapy._private.system_model.fe._2652 import FESubstructureWithBatchOptions
    from mastapy._private.system_model.fe._2653 import FESubstructureWithSelection
    from mastapy._private.system_model.fe._2654 import (
        FESubstructureWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2655 import (
        FESubstructureWithSelectionForHarmonicAnalysis,
    )
    from mastapy._private.system_model.fe._2656 import (
        FESubstructureWithSelectionForModalAnalysis,
    )
    from mastapy._private.system_model.fe._2657 import (
        FESubstructureWithSelectionForStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2658 import GearMeshingOptions
    from mastapy._private.system_model.fe._2659 import (
        IndependentMASTACreatedCondensationNode,
    )
    from mastapy._private.system_model.fe._2660 import (
        IndependentMASTACreatedConstrainedNodes,
    )
    from mastapy._private.system_model.fe._2661 import (
        IndependentMASTACreatedConstrainedNodesWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2662 import (
        IndependentMASTACreatedRigidlyConnectedNodeGroup,
    )
    from mastapy._private.system_model.fe._2663 import (
        LinkComponentAxialPositionErrorReporter,
    )
    from mastapy._private.system_model.fe._2664 import LinkNodeSource
    from mastapy._private.system_model.fe._2665 import MaterialPropertiesWithSelection
    from mastapy._private.system_model.fe._2666 import (
        NodeBoundaryConditionsForFlexibleInterpolationConnection,
    )
    from mastapy._private.system_model.fe._2667 import (
        NodeBoundaryConditionStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2668 import NodeGroupWithSelection
    from mastapy._private.system_model.fe._2669 import NodeSelectionDepthOption
    from mastapy._private.system_model.fe._2670 import NodesForPlanetarySocket
    from mastapy._private.system_model.fe._2671 import NodesForPlanetInSocket
    from mastapy._private.system_model.fe._2672 import (
        OptionsWhenExternalFEFileAlreadyExists,
    )
    from mastapy._private.system_model.fe._2673 import PerLinkExportOptions
    from mastapy._private.system_model.fe._2674 import RaceBearingFE
    from mastapy._private.system_model.fe._2675 import RaceBearingFESystemDeflection
    from mastapy._private.system_model.fe._2676 import RaceBearingFEWithSelection
    from mastapy._private.system_model.fe._2677 import ReplacedShaftSelectionHelper
    from mastapy._private.system_model.fe._2678 import SelectableNodeAtAngle
    from mastapy._private.system_model.fe._2679 import SystemDeflectionFEExportOptions
    from mastapy._private.system_model.fe._2680 import ThermalExpansionOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe._2615": ["AlignConnectedComponentOptions"],
        "_private.system_model.fe._2616": ["AlignmentMethod"],
        "_private.system_model.fe._2617": ["AlignmentMethodForRaceBearing"],
        "_private.system_model.fe._2618": ["AlignmentUsingAxialNodePositions"],
        "_private.system_model.fe._2619": ["AngleSource"],
        "_private.system_model.fe._2620": ["BaseFEWithSelection"],
        "_private.system_model.fe._2621": ["BatchOperations"],
        "_private.system_model.fe._2622": ["BearingNodeAlignmentOption"],
        "_private.system_model.fe._2623": ["BearingNodeOption"],
        "_private.system_model.fe._2624": ["BearingRaceNodeLink"],
        "_private.system_model.fe._2625": ["BearingRacePosition"],
        "_private.system_model.fe._2626": ["ComponentOrientationOption"],
        "_private.system_model.fe._2627": ["ContactPairWithSelection"],
        "_private.system_model.fe._2628": ["CoordinateSystemWithSelection"],
        "_private.system_model.fe._2629": ["CreateConnectedComponentOptions"],
        "_private.system_model.fe._2630": ["CreateMicrophoneNormalToSurfaceOptions"],
        "_private.system_model.fe._2631": ["DegreeOfFreedomBoundaryCondition"],
        "_private.system_model.fe._2632": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_private.system_model.fe._2633": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_private.system_model.fe._2634": ["ElectricMachineDataSet"],
        "_private.system_model.fe._2635": ["ElectricMachineDynamicLoadData"],
        "_private.system_model.fe._2636": ["ElementFaceGroupWithSelection"],
        "_private.system_model.fe._2637": ["ElementPropertiesWithSelection"],
        "_private.system_model.fe._2638": ["ExportOptionsForNode"],
        "_private.system_model.fe._2639": [
            "ExportOptionsForNodeWithBoundaryConditionType"
        ],
        "_private.system_model.fe._2640": ["FEEntityGroupWithSelection"],
        "_private.system_model.fe._2641": ["FEExportSettings"],
        "_private.system_model.fe._2642": ["FEPartDRIVASurfaceSelection"],
        "_private.system_model.fe._2643": ["FEPartWithBatchOptions"],
        "_private.system_model.fe._2644": ["FEStiffnessGeometry"],
        "_private.system_model.fe._2645": ["FEStiffnessTester"],
        "_private.system_model.fe._2646": ["FESubstructure"],
        "_private.system_model.fe._2647": ["FESubstructureExportOptions"],
        "_private.system_model.fe._2648": ["FESubstructureNode"],
        "_private.system_model.fe._2649": ["FESubstructureNodeModeShape"],
        "_private.system_model.fe._2650": ["FESubstructureNodeModeShapes"],
        "_private.system_model.fe._2651": ["FESubstructureType"],
        "_private.system_model.fe._2652": ["FESubstructureWithBatchOptions"],
        "_private.system_model.fe._2653": ["FESubstructureWithSelection"],
        "_private.system_model.fe._2654": ["FESubstructureWithSelectionComponents"],
        "_private.system_model.fe._2655": [
            "FESubstructureWithSelectionForHarmonicAnalysis"
        ],
        "_private.system_model.fe._2656": [
            "FESubstructureWithSelectionForModalAnalysis"
        ],
        "_private.system_model.fe._2657": [
            "FESubstructureWithSelectionForStaticAnalysis"
        ],
        "_private.system_model.fe._2658": ["GearMeshingOptions"],
        "_private.system_model.fe._2659": ["IndependentMASTACreatedCondensationNode"],
        "_private.system_model.fe._2660": ["IndependentMASTACreatedConstrainedNodes"],
        "_private.system_model.fe._2661": [
            "IndependentMASTACreatedConstrainedNodesWithSelectionComponents"
        ],
        "_private.system_model.fe._2662": [
            "IndependentMASTACreatedRigidlyConnectedNodeGroup"
        ],
        "_private.system_model.fe._2663": ["LinkComponentAxialPositionErrorReporter"],
        "_private.system_model.fe._2664": ["LinkNodeSource"],
        "_private.system_model.fe._2665": ["MaterialPropertiesWithSelection"],
        "_private.system_model.fe._2666": [
            "NodeBoundaryConditionsForFlexibleInterpolationConnection"
        ],
        "_private.system_model.fe._2667": ["NodeBoundaryConditionStaticAnalysis"],
        "_private.system_model.fe._2668": ["NodeGroupWithSelection"],
        "_private.system_model.fe._2669": ["NodeSelectionDepthOption"],
        "_private.system_model.fe._2670": ["NodesForPlanetarySocket"],
        "_private.system_model.fe._2671": ["NodesForPlanetInSocket"],
        "_private.system_model.fe._2672": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_private.system_model.fe._2673": ["PerLinkExportOptions"],
        "_private.system_model.fe._2674": ["RaceBearingFE"],
        "_private.system_model.fe._2675": ["RaceBearingFESystemDeflection"],
        "_private.system_model.fe._2676": ["RaceBearingFEWithSelection"],
        "_private.system_model.fe._2677": ["ReplacedShaftSelectionHelper"],
        "_private.system_model.fe._2678": ["SelectableNodeAtAngle"],
        "_private.system_model.fe._2679": ["SystemDeflectionFEExportOptions"],
        "_private.system_model.fe._2680": ["ThermalExpansionOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "CreateMicrophoneNormalToSurfaceOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "ExportOptionsForNode",
    "ExportOptionsForNodeWithBoundaryConditionType",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "IndependentMASTACreatedConstrainedNodes",
    "IndependentMASTACreatedConstrainedNodesWithSelectionComponents",
    "IndependentMASTACreatedRigidlyConnectedNodeGroup",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionsForFlexibleInterpolationConnection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "NodesForPlanetarySocket",
    "NodesForPlanetInSocket",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SelectableNodeAtAngle",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
