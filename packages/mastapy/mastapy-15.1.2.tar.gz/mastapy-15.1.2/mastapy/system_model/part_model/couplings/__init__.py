"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2860 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2861 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2862 import Clutch
    from mastapy._private.system_model.part_model.couplings._2863 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2864 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2865 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2866 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2867 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2868 import Coupling
    from mastapy._private.system_model.part_model.couplings._2869 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2870 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2871 import CVT
    from mastapy._private.system_model.part_model.couplings._2872 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2873 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2874 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2875 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2876 import Pulley
    from mastapy._private.system_model.part_model.couplings._2877 import (
        RigidConnectorSettings,
    )
    from mastapy._private.system_model.part_model.couplings._2878 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2879 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2880 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2881 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2882 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2883 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2884 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2885 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2886 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2887 import (
        SplineHalfManufacturingError,
    )
    from mastapy._private.system_model.part_model.couplings._2888 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2889 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2890 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2891 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2892 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2893 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2894 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2895 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2896 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2897 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2898 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2899 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2900 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2901 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2860": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2861": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2862": ["Clutch"],
        "_private.system_model.part_model.couplings._2863": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2864": ["ClutchType"],
        "_private.system_model.part_model.couplings._2865": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2866": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2867": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2868": ["Coupling"],
        "_private.system_model.part_model.couplings._2869": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2870": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2871": ["CVT"],
        "_private.system_model.part_model.couplings._2872": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2873": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2874": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2875": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2876": ["Pulley"],
        "_private.system_model.part_model.couplings._2877": ["RigidConnectorSettings"],
        "_private.system_model.part_model.couplings._2878": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2879": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2880": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2881": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2882": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2883": ["RollingRing"],
        "_private.system_model.part_model.couplings._2884": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2885": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2886": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2887": [
            "SplineHalfManufacturingError"
        ],
        "_private.system_model.part_model.couplings._2888": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2889": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2890": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2891": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2892": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2893": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2894": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2895": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2896": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2897": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2898": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2899": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2900": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2901": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorSettings",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineHalfManufacturingError",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
