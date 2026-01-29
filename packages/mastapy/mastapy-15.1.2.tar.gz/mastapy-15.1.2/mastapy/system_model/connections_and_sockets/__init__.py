"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets._2525 import (
        AbstractShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2526 import (
        BearingInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2527 import (
        BearingOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2528 import (
        BeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2529 import (
        CoaxialConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2530 import (
        ComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2531 import (
        ComponentMeasurer,
    )
    from mastapy._private.system_model.connections_and_sockets._2532 import Connection
    from mastapy._private.system_model.connections_and_sockets._2533 import (
        CVTBeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2534 import (
        CVTPulleySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2535 import (
        CylindricalComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2536 import (
        CylindricalSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2537 import (
        DatumMeasurement,
    )
    from mastapy._private.system_model.connections_and_sockets._2538 import (
        ElectricMachineStatorSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2539 import (
        InnerShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2540 import (
        InnerShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2541 import (
        InterMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2542 import (
        MountableComponentInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2543 import (
        MountableComponentOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2544 import (
        MountableComponentSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2545 import (
        OuterShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2546 import (
        OuterShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2547 import (
        PlanetaryConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2548 import (
        PlanetarySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2549 import (
        PlanetarySocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2550 import PulleySocket
    from mastapy._private.system_model.connections_and_sockets._2551 import (
        RealignmentResult,
    )
    from mastapy._private.system_model.connections_and_sockets._2552 import (
        RollingRingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2553 import (
        RollingRingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2554 import ShaftSocket
    from mastapy._private.system_model.connections_and_sockets._2555 import (
        ShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2556 import Socket
    from mastapy._private.system_model.connections_and_sockets._2557 import (
        SocketConnectionOptions,
    )
    from mastapy._private.system_model.connections_and_sockets._2558 import (
        SocketConnectionSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets._2525": [
            "AbstractShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2526": ["BearingInnerSocket"],
        "_private.system_model.connections_and_sockets._2527": ["BearingOuterSocket"],
        "_private.system_model.connections_and_sockets._2528": ["BeltConnection"],
        "_private.system_model.connections_and_sockets._2529": ["CoaxialConnection"],
        "_private.system_model.connections_and_sockets._2530": ["ComponentConnection"],
        "_private.system_model.connections_and_sockets._2531": ["ComponentMeasurer"],
        "_private.system_model.connections_and_sockets._2532": ["Connection"],
        "_private.system_model.connections_and_sockets._2533": ["CVTBeltConnection"],
        "_private.system_model.connections_and_sockets._2534": ["CVTPulleySocket"],
        "_private.system_model.connections_and_sockets._2535": [
            "CylindricalComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2536": ["CylindricalSocket"],
        "_private.system_model.connections_and_sockets._2537": ["DatumMeasurement"],
        "_private.system_model.connections_and_sockets._2538": [
            "ElectricMachineStatorSocket"
        ],
        "_private.system_model.connections_and_sockets._2539": ["InnerShaftSocket"],
        "_private.system_model.connections_and_sockets._2540": ["InnerShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2541": [
            "InterMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2542": [
            "MountableComponentInnerSocket"
        ],
        "_private.system_model.connections_and_sockets._2543": [
            "MountableComponentOuterSocket"
        ],
        "_private.system_model.connections_and_sockets._2544": [
            "MountableComponentSocket"
        ],
        "_private.system_model.connections_and_sockets._2545": ["OuterShaftSocket"],
        "_private.system_model.connections_and_sockets._2546": ["OuterShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2547": ["PlanetaryConnection"],
        "_private.system_model.connections_and_sockets._2548": ["PlanetarySocket"],
        "_private.system_model.connections_and_sockets._2549": ["PlanetarySocketBase"],
        "_private.system_model.connections_and_sockets._2550": ["PulleySocket"],
        "_private.system_model.connections_and_sockets._2551": ["RealignmentResult"],
        "_private.system_model.connections_and_sockets._2552": [
            "RollingRingConnection"
        ],
        "_private.system_model.connections_and_sockets._2553": ["RollingRingSocket"],
        "_private.system_model.connections_and_sockets._2554": ["ShaftSocket"],
        "_private.system_model.connections_and_sockets._2555": [
            "ShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2556": ["Socket"],
        "_private.system_model.connections_and_sockets._2557": [
            "SocketConnectionOptions"
        ],
        "_private.system_model.connections_and_sockets._2558": [
            "SocketConnectionSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftToMountableComponentConnection",
    "BearingInnerSocket",
    "BearingOuterSocket",
    "BeltConnection",
    "CoaxialConnection",
    "ComponentConnection",
    "ComponentMeasurer",
    "Connection",
    "CVTBeltConnection",
    "CVTPulleySocket",
    "CylindricalComponentConnection",
    "CylindricalSocket",
    "DatumMeasurement",
    "ElectricMachineStatorSocket",
    "InnerShaftSocket",
    "InnerShaftSocketBase",
    "InterMountableComponentConnection",
    "MountableComponentInnerSocket",
    "MountableComponentOuterSocket",
    "MountableComponentSocket",
    "OuterShaftSocket",
    "OuterShaftSocketBase",
    "PlanetaryConnection",
    "PlanetarySocket",
    "PlanetarySocketBase",
    "PulleySocket",
    "RealignmentResult",
    "RollingRingConnection",
    "RollingRingSocket",
    "ShaftSocket",
    "ShaftToMountableComponentConnection",
    "Socket",
    "SocketConnectionOptions",
    "SocketConnectionSelection",
)
