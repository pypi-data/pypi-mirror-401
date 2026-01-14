"""Type stubs for QOS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .dot1p_map import Dot1pMap, Dot1pMapDictMode, Dot1pMapObjectMode
    from .ip_dscp_map import IpDscpMap, IpDscpMapDictMode, IpDscpMapObjectMode
    from .qos_policy import QosPolicy, QosPolicyDictMode, QosPolicyObjectMode
    from .queue_policy import QueuePolicy, QueuePolicyDictMode, QueuePolicyObjectMode

__all__ = [
    "Dot1pMap",
    "IpDscpMap",
    "QosPolicy",
    "QueuePolicy",
    "QosDictMode",
    "QosObjectMode",
]

class QosDictMode:
    """QOS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    dot1p_map: Dot1pMapDictMode
    ip_dscp_map: IpDscpMapDictMode
    qos_policy: QosPolicyDictMode
    queue_policy: QueuePolicyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize qos category with HTTP client."""
        ...


class QosObjectMode:
    """QOS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    dot1p_map: Dot1pMapObjectMode
    ip_dscp_map: IpDscpMapObjectMode
    qos_policy: QosPolicyObjectMode
    queue_policy: QueuePolicyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize qos category with HTTP client."""
        ...


# Base class for backwards compatibility
class Qos:
    """QOS API category."""
    
    dot1p_map: Dot1pMap
    ip_dscp_map: IpDscpMap
    qos_policy: QosPolicy
    queue_policy: QueuePolicy

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize qos category with HTTP client."""
        ...
