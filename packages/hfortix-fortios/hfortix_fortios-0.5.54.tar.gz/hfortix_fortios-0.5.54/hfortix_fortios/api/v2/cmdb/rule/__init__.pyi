"""Type stubs for RULE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .fmwp import Fmwp, FmwpDictMode, FmwpObjectMode
    from .iotd import Iotd, IotdDictMode, IotdObjectMode
    from .otdt import Otdt, OtdtDictMode, OtdtObjectMode
    from .otvp import Otvp, OtvpDictMode, OtvpObjectMode

__all__ = [
    "Fmwp",
    "Iotd",
    "Otdt",
    "Otvp",
    "RuleDictMode",
    "RuleObjectMode",
]

class RuleDictMode:
    """RULE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    fmwp: FmwpDictMode
    iotd: IotdDictMode
    otdt: OtdtDictMode
    otvp: OtvpDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize rule category with HTTP client."""
        ...


class RuleObjectMode:
    """RULE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    fmwp: FmwpObjectMode
    iotd: IotdObjectMode
    otdt: OtdtObjectMode
    otvp: OtvpObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize rule category with HTTP client."""
        ...


# Base class for backwards compatibility
class Rule:
    """RULE API category."""
    
    fmwp: Fmwp
    iotd: Iotd
    otdt: Otdt
    otvp: Otvp

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize rule category with HTTP client."""
        ...
