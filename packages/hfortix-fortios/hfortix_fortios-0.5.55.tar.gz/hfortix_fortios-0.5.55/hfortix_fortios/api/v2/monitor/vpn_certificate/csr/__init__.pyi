"""Type stubs for CSR category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .generate import Generate, GenerateDictMode, GenerateObjectMode

__all__ = [
    "Generate",
    "CsrDictMode",
    "CsrObjectMode",
]

class CsrDictMode:
    """CSR API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    generate: GenerateDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize csr category with HTTP client."""
        ...


class CsrObjectMode:
    """CSR API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    generate: GenerateObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize csr category with HTTP client."""
        ...


# Base class for backwards compatibility
class Csr:
    """CSR API category."""
    
    generate: Generate

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize csr category with HTTP client."""
        ...
