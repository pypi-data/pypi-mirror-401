"""
FortiOS LOG API - Disk

Log query endpoints for disk logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They accept path parameters that are represented as nested classes.

Example Usage:
    >>> fgt.api.log.disk.event.vpn.get(rows=100)
    >>> fgt.api.log.disk.traffic.forward.get(rows=50)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from hfortix_core.http.interface import IHTTPClient


class Disk:
    """Disk log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize Disk endpoint."""
        self._client = client
        self.anomaly = DiskAnomaly(client)
        self.app_ctrl = DiskAppCtrl(client)
        self.cifs = DiskCifs(client)
        self.dlp = DiskDlp(client)
        self.dns = DiskDns(client)
        self.emailfilter = DiskEmailfilter(client)
        self.event = DiskEvent(client)
        self.file_filter = DiskFileFilter(client)
        self.gtp = DiskGtp(client)
        self.ips = DiskIps(client)
        self.ssh = DiskSsh(client)
        self.ssl = DiskSsl(client)
        self.traffic = DiskTraffic(client)
        self.virus = DiskVirus(client)
        self.voip = DiskVoip(client)
        self.waf = DiskWaf(client)
        self.webfilter = DiskWebfilter(client)


class DiskAnomaly:
    """DiskAnomaly log operations (type=anomaly)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskAnomaly."""
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
        return self._client.get("log", "/log/disk/anomaly/raw", **kwargs)


class DiskAppCtrl:
    """DiskAppCtrl log operations (type=app-ctrl)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskAppCtrl."""
        self._client = client
        self.archive = DiskAppCtrlArchive(client, "app-ctrl")
        self.archive_download = DiskAppCtrlArchiveDownload(client, "app-ctrl")

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
        return self._client.get("log", "/log/disk/app-ctrl/raw", **kwargs)


class DiskAppCtrlArchive:
    """archive operations for app_ctrl."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize DiskAppCtrlArchive."""
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
        return self._client.get("log", "/log/disk/app-ctrl/archive", **kwargs)


class DiskAppCtrlArchiveDownload:
    """archive-download operations for app_ctrl."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize DiskAppCtrlArchiveDownload."""
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
        return self._client.get("log", "/log/disk/app-ctrl/archive-download", **kwargs)


class DiskCifs:
    """DiskCifs log operations (type=cifs)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskCifs."""
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
        return self._client.get("log", "/log/disk/cifs/raw", **kwargs)


class DiskDlp:
    """DiskDlp log operations (type=dlp)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskDlp."""
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
        return self._client.get("log", "/log/disk/dlp/raw", **kwargs)


class DiskDns:
    """DiskDns log operations (type=dns)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskDns."""
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
        return self._client.get("log", "/log/disk/dns/raw", **kwargs)


class DiskEmailfilter:
    """DiskEmailfilter log operations (type=emailfilter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEmailfilter."""
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
        return self._client.get("log", "/log/disk/emailfilter/raw", **kwargs)


class DiskEvent:
    """DiskEvent log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEvent."""
        self._client = client
        self.compliance_check = DiskEventComplianceCheck(client, "compliance-check")
        self.connector = DiskEventConnector(client, "connector")
        self.endpoint = DiskEventEndpoint(client, "endpoint")
        self.fortiextender = DiskEventFortiextender(client, "fortiextender")
        self.ha = DiskEventHa(client, "ha")
        self.router = DiskEventRouter(client, "router")
        self.security_rating = DiskEventSecurityRating(client, "security-rating")
        self.system = DiskEventSystem(client, "system")
        self.user = DiskEventUser(client, "user")
        self.vpn = DiskEventVpn(client, "vpn")
        self.wad = DiskEventWad(client, "wad")
        self.wireless = DiskEventWireless(client, "wireless")


class DiskEventComplianceCheck:
    """event logs for compliance-check."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventComplianceCheck."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventConnector:
    """event logs for connector."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventConnector."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventEndpoint:
    """event logs for endpoint."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventEndpoint."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventFortiextender:
    """event logs for fortiextender."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventFortiextender."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventHa:
    """event logs for ha."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventHa."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventRouter:
    """event logs for router."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventRouter."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventSecurityRating:
    """event logs for security-rating."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventSecurityRating."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventSystem:
    """event logs for system."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventSystem."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventUser:
    """event logs for user."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventUser."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventVpn:
    """event logs for vpn."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventVpn."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventWad:
    """event logs for wad."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventWad."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskEventWireless:
    """event logs for wireless."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskEventWireless."""
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
        return self._client.get("log", f"/log/disk/event/{self._subtype}/raw", **kwargs)


class DiskFileFilter:
    """DiskFileFilter log operations (type=file-filter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskFileFilter."""
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
        return self._client.get("log", "/log/disk/file-filter/raw", **kwargs)


class DiskGtp:
    """DiskGtp log operations (type=gtp)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskGtp."""
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
        return self._client.get("log", "/log/disk/gtp/raw", **kwargs)


class DiskIps:
    """DiskIps log operations (type=ips)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskIps."""
        self._client = client
        self.archive = DiskIpsArchive(client, "ips")
        self.archive_download = DiskIpsArchiveDownload(client, "ips")

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
        return self._client.get("log", "/log/disk/ips/raw", **kwargs)


class DiskIpsArchive:
    """archive operations for ips."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize DiskIpsArchive."""
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
        return self._client.get("log", "/log/disk/ips/archive", **kwargs)


class DiskIpsArchiveDownload:
    """archive-download operations for ips."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize DiskIpsArchiveDownload."""
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
        return self._client.get("log", "/log/disk/ips/archive-download", **kwargs)


class DiskSsh:
    """DiskSsh log operations (type=ssh)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskSsh."""
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
        return self._client.get("log", "/log/disk/ssh/raw", **kwargs)


class DiskSsl:
    """DiskSsl log operations (type=ssl)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskSsl."""
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
        return self._client.get("log", "/log/disk/ssl/raw", **kwargs)


class DiskTraffic:
    """DiskTraffic log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTraffic."""
        self._client = client
        self.fortiview = DiskTrafficFortiview(client, "fortiview")
        self.forward = DiskTrafficForward(client, "forward")
        self.local = DiskTrafficLocal(client, "local")
        self.multicast = DiskTrafficMulticast(client, "multicast")
        self.sniffer = DiskTrafficSniffer(client, "sniffer")
        self.threat = DiskTrafficThreat(client, "threat")


class DiskTrafficFortiview:
    """traffic logs for fortiview."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskTrafficFortiview."""
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
        return self._client.get("log", f"/log/disk/traffic/{self._subtype}/raw", **kwargs)


class DiskTrafficForward:
    """traffic logs for forward."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskTrafficForward."""
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
        return self._client.get("log", f"/log/disk/traffic/{self._subtype}/raw", **kwargs)


class DiskTrafficLocal:
    """traffic logs for local."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskTrafficLocal."""
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
        return self._client.get("log", f"/log/disk/traffic/{self._subtype}/raw", **kwargs)


class DiskTrafficMulticast:
    """traffic logs for multicast."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskTrafficMulticast."""
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
        return self._client.get("log", f"/log/disk/traffic/{self._subtype}/raw", **kwargs)


class DiskTrafficSniffer:
    """traffic logs for sniffer."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskTrafficSniffer."""
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
        return self._client.get("log", f"/log/disk/traffic/{self._subtype}/raw", **kwargs)


class DiskTrafficThreat:
    """traffic logs for threat."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize DiskTrafficThreat."""
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
        return self._client.get("log", f"/log/disk/traffic/{self._subtype}/raw", **kwargs)


class DiskVirus:
    """DiskVirus log operations (type=virus)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskVirus."""
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
        return self._client.get("log", "/log/disk/virus/raw", **kwargs)


class DiskVoip:
    """DiskVoip log operations (type=voip)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskVoip."""
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
        return self._client.get("log", "/log/disk/voip/raw", **kwargs)


class DiskWaf:
    """DiskWaf log operations (type=waf)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskWaf."""
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
        return self._client.get("log", "/log/disk/waf/raw", **kwargs)


class DiskWebfilter:
    """DiskWebfilter log operations (type=webfilter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskWebfilter."""
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
        return self._client.get("log", "/log/disk/webfilter/raw", **kwargs)
