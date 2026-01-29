"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets.couplings._2602 import (
        ClutchConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2603 import (
        ClutchSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2604 import (
        ConceptCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2605 import (
        ConceptCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2606 import (
        CouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2607 import (
        CouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2608 import (
        PartToPartShearCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2609 import (
        PartToPartShearCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2610 import (
        SpringDamperConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2611 import (
        SpringDamperSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2612 import (
        TorqueConverterConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2613 import (
        TorqueConverterPumpSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2614 import (
        TorqueConverterTurbineSocket,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets.couplings._2602": [
            "ClutchConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2603": [
            "ClutchSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2604": [
            "ConceptCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2605": [
            "ConceptCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2606": [
            "CouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2607": [
            "CouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2608": [
            "PartToPartShearCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2609": [
            "PartToPartShearCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2610": [
            "SpringDamperConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2611": [
            "SpringDamperSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2612": [
            "TorqueConverterConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2613": [
            "TorqueConverterPumpSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2614": [
            "TorqueConverterTurbineSocket"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ClutchConnection",
    "ClutchSocket",
    "ConceptCouplingConnection",
    "ConceptCouplingSocket",
    "CouplingConnection",
    "CouplingSocket",
    "PartToPartShearCouplingConnection",
    "PartToPartShearCouplingSocket",
    "SpringDamperConnection",
    "SpringDamperSocket",
    "TorqueConverterConnection",
    "TorqueConverterPumpSocket",
    "TorqueConverterTurbineSocket",
)
