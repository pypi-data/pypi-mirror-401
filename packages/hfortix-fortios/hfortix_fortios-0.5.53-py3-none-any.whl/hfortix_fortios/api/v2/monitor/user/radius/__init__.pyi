"""Type stubs for RADIUS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .get_test_connect import GetTestConnect, GetTestConnectDictMode, GetTestConnectObjectMode
    from .test_connect import TestConnect, TestConnectDictMode, TestConnectObjectMode

__all__ = [
    "GetTestConnect",
    "TestConnect",
    "RadiusDictMode",
    "RadiusObjectMode",
]

class RadiusDictMode:
    """RADIUS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    get_test_connect: GetTestConnectDictMode
    test_connect: TestConnectDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize radius category with HTTP client."""
        ...


class RadiusObjectMode:
    """RADIUS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    get_test_connect: GetTestConnectObjectMode
    test_connect: TestConnectObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize radius category with HTTP client."""
        ...


# Base class for backwards compatibility
class Radius:
    """RADIUS API category."""
    
    get_test_connect: GetTestConnect
    test_connect: TestConnect

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize radius category with HTTP client."""
        ...
