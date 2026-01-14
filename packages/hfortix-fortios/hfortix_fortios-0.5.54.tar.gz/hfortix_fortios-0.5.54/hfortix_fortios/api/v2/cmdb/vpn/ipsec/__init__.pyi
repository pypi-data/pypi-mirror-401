"""Type stubs for IPSEC category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .concentrator import Concentrator, ConcentratorDictMode, ConcentratorObjectMode
    from .fec import Fec, FecDictMode, FecObjectMode
    from .manualkey import Manualkey, ManualkeyDictMode, ManualkeyObjectMode
    from .manualkey_interface import ManualkeyInterface, ManualkeyInterfaceDictMode, ManualkeyInterfaceObjectMode
    from .phase1 import Phase1, Phase1DictMode, Phase1ObjectMode
    from .phase1_interface import Phase1Interface, Phase1InterfaceDictMode, Phase1InterfaceObjectMode
    from .phase2 import Phase2, Phase2DictMode, Phase2ObjectMode
    from .phase2_interface import Phase2Interface, Phase2InterfaceDictMode, Phase2InterfaceObjectMode

__all__ = [
    "Concentrator",
    "Fec",
    "Manualkey",
    "ManualkeyInterface",
    "Phase1",
    "Phase1Interface",
    "Phase2",
    "Phase2Interface",
    "IpsecDictMode",
    "IpsecObjectMode",
]

class IpsecDictMode:
    """IPSEC API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    concentrator: ConcentratorDictMode
    fec: FecDictMode
    manualkey: ManualkeyDictMode
    manualkey_interface: ManualkeyInterfaceDictMode
    phase1: Phase1DictMode
    phase1_interface: Phase1InterfaceDictMode
    phase2: Phase2DictMode
    phase2_interface: Phase2InterfaceDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipsec category with HTTP client."""
        ...


class IpsecObjectMode:
    """IPSEC API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    concentrator: ConcentratorObjectMode
    fec: FecObjectMode
    manualkey: ManualkeyObjectMode
    manualkey_interface: ManualkeyInterfaceObjectMode
    phase1: Phase1ObjectMode
    phase1_interface: Phase1InterfaceObjectMode
    phase2: Phase2ObjectMode
    phase2_interface: Phase2InterfaceObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipsec category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ipsec:
    """IPSEC API category."""
    
    concentrator: Concentrator
    fec: Fec
    manualkey: Manualkey
    manualkey_interface: ManualkeyInterface
    phase1: Phase1
    phase1_interface: Phase1Interface
    phase2: Phase2
    phase2_interface: Phase2Interface

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipsec category with HTTP client."""
        ...
