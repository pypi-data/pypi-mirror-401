"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.import_from_cad._2773 import (
        AbstractShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2774 import (
        ClutchFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2775 import (
        ComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2776 import (
        ComponentFromCADBase,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2777 import (
        ConceptBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2778 import (
        ConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2779 import (
        CylindricalGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2780 import (
        CylindricalGearInPlanetarySetFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2781 import (
        CylindricalPlanetGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2782 import (
        CylindricalRingGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2783 import (
        CylindricalSunGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2784 import (
        HousedOrMounted,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2785 import (
        MountableComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2786 import (
        PlanetShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2787 import (
        PulleyFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2788 import (
        RigidConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2789 import (
        RollingBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2790 import (
        ShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2791 import (
        ShaftFromCADAuto,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.import_from_cad._2773": [
            "AbstractShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2774": ["ClutchFromCAD"],
        "_private.system_model.part_model.import_from_cad._2775": ["ComponentFromCAD"],
        "_private.system_model.part_model.import_from_cad._2776": [
            "ComponentFromCADBase"
        ],
        "_private.system_model.part_model.import_from_cad._2777": [
            "ConceptBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2778": ["ConnectorFromCAD"],
        "_private.system_model.part_model.import_from_cad._2779": [
            "CylindricalGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2780": [
            "CylindricalGearInPlanetarySetFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2781": [
            "CylindricalPlanetGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2782": [
            "CylindricalRingGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2783": [
            "CylindricalSunGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2784": ["HousedOrMounted"],
        "_private.system_model.part_model.import_from_cad._2785": [
            "MountableComponentFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2786": [
            "PlanetShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2787": ["PulleyFromCAD"],
        "_private.system_model.part_model.import_from_cad._2788": [
            "RigidConnectorFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2789": [
            "RollingBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2790": ["ShaftFromCAD"],
        "_private.system_model.part_model.import_from_cad._2791": ["ShaftFromCADAuto"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftFromCAD",
    "ClutchFromCAD",
    "ComponentFromCAD",
    "ComponentFromCADBase",
    "ConceptBearingFromCAD",
    "ConnectorFromCAD",
    "CylindricalGearFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
    "CylindricalPlanetGearFromCAD",
    "CylindricalRingGearFromCAD",
    "CylindricalSunGearFromCAD",
    "HousedOrMounted",
    "MountableComponentFromCAD",
    "PlanetShaftFromCAD",
    "PulleyFromCAD",
    "RigidConnectorFromCAD",
    "RollingBearingFromCAD",
    "ShaftFromCAD",
    "ShaftFromCADAuto",
)
