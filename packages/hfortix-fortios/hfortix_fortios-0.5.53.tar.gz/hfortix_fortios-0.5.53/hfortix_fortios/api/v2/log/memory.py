"""
FortiOS LOG API - Memory

Log query endpoints for memory logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They accept path parameters that are represented as nested classes.

Example Usage:
    >>> fgt.api.log.memory.event.vpn.get(rows=100)
    >>> fgt.api.log.memory.traffic.forward.get(rows=50)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from hfortix_core.http.interface import IHTTPClient


class Memory:
    """Memory log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize Memory endpoint."""
        self._client = client
        self.anomaly = MemoryAnomaly(client)
        self.app_ctrl = MemoryAppCtrl(client)
        self.cifs = MemoryCifs(client)
        self.dlp = MemoryDlp(client)
        self.dns = MemoryDns(client)
        self.emailfilter = MemoryEmailfilter(client)
        self.event = MemoryEvent(client)
        self.file_filter = MemoryFileFilter(client)
        self.gtp = MemoryGtp(client)
        self.ips = MemoryIps(client)
        self.ssh = MemorySsh(client)
        self.ssl = MemorySsl(client)
        self.traffic = MemoryTraffic(client)
        self.virus = MemoryVirus(client)
        self.voip = MemoryVoip(client)
        self.waf = MemoryWaf(client)
        self.webfilter = MemoryWebfilter(client)


class MemoryAnomaly:
    """MemoryAnomaly log operations (type=anomaly)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryAnomaly."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get anomaly logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/anomaly/raw", **kwargs)


class MemoryAppCtrl:
    """MemoryAppCtrl log operations (type=app-ctrl)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryAppCtrl."""
        self._client = client
        self.archive = MemoryAppCtrlArchive(client, "app-ctrl")
        self.archive_download = MemoryAppCtrlArchiveDownload(client, "app-ctrl")

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get app_ctrl logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/app-ctrl/raw", **kwargs)


class MemoryAppCtrlArchive:
    """archive operations for app_ctrl."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize MemoryAppCtrlArchive."""
        self._client = client
        self._type = type_value

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get archive data for this log type.
        
        Args:
            **kwargs: Additional query parameters
        
        Returns:
            Dict containing archive data
        """
        return self._client.get("log", "/log/memory/app-ctrl/archive", **kwargs)


class MemoryAppCtrlArchiveDownload:
    """archive-download operations for app_ctrl."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize MemoryAppCtrlArchiveDownload."""
        self._client = client
        self._type = type_value

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get archive-download data for this log type.
        
        Args:
            **kwargs: Additional query parameters
        
        Returns:
            Dict containing archive-download data
        """
        return self._client.get("log", "/log/memory/app-ctrl/archive-download", **kwargs)


class MemoryCifs:
    """MemoryCifs log operations (type=cifs)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryCifs."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get cifs logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/cifs/raw", **kwargs)


class MemoryDlp:
    """MemoryDlp log operations (type=dlp)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryDlp."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get dlp logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/dlp/raw", **kwargs)


class MemoryDns:
    """MemoryDns log operations (type=dns)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryDns."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get dns logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/dns/raw", **kwargs)


class MemoryEmailfilter:
    """MemoryEmailfilter log operations (type=emailfilter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEmailfilter."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get emailfilter logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/emailfilter/raw", **kwargs)


class MemoryEvent:
    """MemoryEvent log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEvent."""
        self._client = client
        self.compliance_check = MemoryEventComplianceCheck(client, "compliance-check")
        self.connector = MemoryEventConnector(client, "connector")
        self.endpoint = MemoryEventEndpoint(client, "endpoint")
        self.fortiextender = MemoryEventFortiextender(client, "fortiextender")
        self.ha = MemoryEventHa(client, "ha")
        self.router = MemoryEventRouter(client, "router")
        self.security_rating = MemoryEventSecurityRating(client, "security-rating")
        self.system = MemoryEventSystem(client, "system")
        self.user = MemoryEventUser(client, "user")
        self.vpn = MemoryEventVpn(client, "vpn")
        self.wad = MemoryEventWad(client, "wad")
        self.wireless = MemoryEventWireless(client, "wireless")


class MemoryEventComplianceCheck:
    """event logs for compliance-check."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventComplianceCheck."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get compliance-check event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventConnector:
    """event logs for connector."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventConnector."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get connector event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventEndpoint:
    """event logs for endpoint."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventEndpoint."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get endpoint event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventFortiextender:
    """event logs for fortiextender."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventFortiextender."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get fortiextender event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventHa:
    """event logs for ha."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventHa."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get ha event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventRouter:
    """event logs for router."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventRouter."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get router event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventSecurityRating:
    """event logs for security-rating."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventSecurityRating."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get security-rating event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventSystem:
    """event logs for system."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventSystem."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get system event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventUser:
    """event logs for user."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventUser."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get user event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventVpn:
    """event logs for vpn."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventVpn."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get vpn event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventWad:
    """event logs for wad."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventWad."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get wad event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryEventWireless:
    """event logs for wireless."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryEventWireless."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get wireless event logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/event/{self._subtype}/raw", **kwargs)


class MemoryFileFilter:
    """MemoryFileFilter log operations (type=file-filter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryFileFilter."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get file_filter logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/file-filter/raw", **kwargs)


class MemoryGtp:
    """MemoryGtp log operations (type=gtp)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryGtp."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get gtp logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/gtp/raw", **kwargs)


class MemoryIps:
    """MemoryIps log operations (type=ips)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryIps."""
        self._client = client
        self.archive = MemoryIpsArchive(client, "ips")
        self.archive_download = MemoryIpsArchiveDownload(client, "ips")

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get ips logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/ips/raw", **kwargs)


class MemoryIpsArchive:
    """archive operations for ips."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize MemoryIpsArchive."""
        self._client = client
        self._type = type_value

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get archive data for this log type.
        
        Args:
            **kwargs: Additional query parameters
        
        Returns:
            Dict containing archive data
        """
        return self._client.get("log", "/log/memory/ips/archive", **kwargs)


class MemoryIpsArchiveDownload:
    """archive-download operations for ips."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize MemoryIpsArchiveDownload."""
        self._client = client
        self._type = type_value

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get archive-download data for this log type.
        
        Args:
            **kwargs: Additional query parameters
        
        Returns:
            Dict containing archive-download data
        """
        return self._client.get("log", "/log/memory/ips/archive-download", **kwargs)


class MemorySsh:
    """MemorySsh log operations (type=ssh)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemorySsh."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get ssh logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/ssh/raw", **kwargs)


class MemorySsl:
    """MemorySsl log operations (type=ssl)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemorySsl."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get ssl logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/ssl/raw", **kwargs)


class MemoryTraffic:
    """MemoryTraffic log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTraffic."""
        self._client = client
        self.fortiview = MemoryTrafficFortiview(client, "fortiview")
        self.forward = MemoryTrafficForward(client, "forward")
        self.local = MemoryTrafficLocal(client, "local")
        self.multicast = MemoryTrafficMulticast(client, "multicast")
        self.sniffer = MemoryTrafficSniffer(client, "sniffer")
        self.threat = MemoryTrafficThreat(client, "threat")


class MemoryTrafficFortiview:
    """traffic logs for fortiview."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryTrafficFortiview."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get fortiview traffic logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/traffic/{self._subtype}/raw", **kwargs)


class MemoryTrafficForward:
    """traffic logs for forward."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryTrafficForward."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get forward traffic logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/traffic/{self._subtype}/raw", **kwargs)


class MemoryTrafficLocal:
    """traffic logs for local."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryTrafficLocal."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get local traffic logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/traffic/{self._subtype}/raw", **kwargs)


class MemoryTrafficMulticast:
    """traffic logs for multicast."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryTrafficMulticast."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get multicast traffic logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/traffic/{self._subtype}/raw", **kwargs)


class MemoryTrafficSniffer:
    """traffic logs for sniffer."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryTrafficSniffer."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get sniffer traffic logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/traffic/{self._subtype}/raw", **kwargs)


class MemoryTrafficThreat:
    """traffic logs for threat."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize MemoryTrafficThreat."""
        self._client = client
        self._subtype = subtype

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get threat traffic logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return (default: 100)
                session_id (int): Session ID for paginated retrieval
                filter (str): Filter expression (e.g., "srcip==192.168.1.1")
                serial_no (str): Retrieve logs from specific device
        
        Returns:
            Dict with log records and metadata
        """
        return self._client.get("log", f"/log/memory/traffic/{self._subtype}/raw", **kwargs)


class MemoryVirus:
    """MemoryVirus log operations (type=virus)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryVirus."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get virus logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/virus/raw", **kwargs)


class MemoryVoip:
    """MemoryVoip log operations (type=voip)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryVoip."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get voip logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/voip/raw", **kwargs)


class MemoryWaf:
    """MemoryWaf log operations (type=waf)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryWaf."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get waf logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/waf/raw", **kwargs)


class MemoryWebfilter:
    """MemoryWebfilter log operations (type=webfilter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryWebfilter."""
        self._client = client

    def get(self, **kwargs: Any) -> Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]:
        """
        Get webfilter logs.
        
        Args:
            **kwargs: Query parameters:
                rows (int): Number of log rows to return
                session_id (int): Session ID for continued retrieval
                filter (str): Filter expression(s)
        
        Returns:
            Dict containing log records
        """
        return self._client.get("log", "/log/memory/webfilter/raw", **kwargs)
