"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.links._2687 import FELink
    from mastapy._private.system_model.fe.links._2688 import ElectricMachineStatorFELink
    from mastapy._private.system_model.fe.links._2689 import FELinkWithSelection
    from mastapy._private.system_model.fe.links._2690 import (
        FlexibleInterpolationDefinitionSettings,
    )
    from mastapy._private.system_model.fe.links._2691 import GearMeshFELink
    from mastapy._private.system_model.fe.links._2692 import (
        GearWithDuplicatedMeshesFELink,
    )
    from mastapy._private.system_model.fe.links._2693 import MultiAngleConnectionFELink
    from mastapy._private.system_model.fe.links._2694 import MultiNodeConnectorFELink
    from mastapy._private.system_model.fe.links._2695 import MultiNodeFELink
    from mastapy._private.system_model.fe.links._2696 import (
        PlanetaryConnectorMultiNodeFELink,
    )
    from mastapy._private.system_model.fe.links._2697 import PlanetBasedFELink
    from mastapy._private.system_model.fe.links._2698 import PlanetCarrierFELink
    from mastapy._private.system_model.fe.links._2699 import PointLoadFELink
    from mastapy._private.system_model.fe.links._2700 import RollingRingConnectionFELink
    from mastapy._private.system_model.fe.links._2701 import ShaftHubConnectionFELink
    from mastapy._private.system_model.fe.links._2702 import SingleNodeFELink
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.links._2687": ["FELink"],
        "_private.system_model.fe.links._2688": ["ElectricMachineStatorFELink"],
        "_private.system_model.fe.links._2689": ["FELinkWithSelection"],
        "_private.system_model.fe.links._2690": [
            "FlexibleInterpolationDefinitionSettings"
        ],
        "_private.system_model.fe.links._2691": ["GearMeshFELink"],
        "_private.system_model.fe.links._2692": ["GearWithDuplicatedMeshesFELink"],
        "_private.system_model.fe.links._2693": ["MultiAngleConnectionFELink"],
        "_private.system_model.fe.links._2694": ["MultiNodeConnectorFELink"],
        "_private.system_model.fe.links._2695": ["MultiNodeFELink"],
        "_private.system_model.fe.links._2696": ["PlanetaryConnectorMultiNodeFELink"],
        "_private.system_model.fe.links._2697": ["PlanetBasedFELink"],
        "_private.system_model.fe.links._2698": ["PlanetCarrierFELink"],
        "_private.system_model.fe.links._2699": ["PointLoadFELink"],
        "_private.system_model.fe.links._2700": ["RollingRingConnectionFELink"],
        "_private.system_model.fe.links._2701": ["ShaftHubConnectionFELink"],
        "_private.system_model.fe.links._2702": ["SingleNodeFELink"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FELink",
    "ElectricMachineStatorFELink",
    "FELinkWithSelection",
    "FlexibleInterpolationDefinitionSettings",
    "GearMeshFELink",
    "GearWithDuplicatedMeshesFELink",
    "MultiAngleConnectionFELink",
    "MultiNodeConnectorFELink",
    "MultiNodeFELink",
    "PlanetaryConnectorMultiNodeFELink",
    "PlanetBasedFELink",
    "PlanetCarrierFELink",
    "PointLoadFELink",
    "RollingRingConnectionFELink",
    "ShaftHubConnectionFELink",
    "SingleNodeFELink",
)
