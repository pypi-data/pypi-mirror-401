"""
FortiOS LOG API - Fortianalyzer

Log query endpoints for fortianalyzer logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They accept path parameters that are represented as nested classes.

Example Usage:
    >>> fgt.api.log.fortianalyzer.event.vpn.get(rows=100)
    >>> fgt.api.log.fortianalyzer.traffic.forward.get(rows=50)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from hfortix_core.http.interface import IHTTPClient


class Fortianalyzer:
    """Fortianalyzer log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize Fortianalyzer endpoint."""
        self._client = client
        self.anomaly = FortianalyzerAnomaly(client)
        self.app_ctrl = FortianalyzerAppCtrl(client)
        self.cifs = FortianalyzerCifs(client)
        self.dlp = FortianalyzerDlp(client)
        self.dns = FortianalyzerDns(client)
        self.emailfilter = FortianalyzerEmailfilter(client)
        self.event = FortianalyzerEvent(client)
        self.file_filter = FortianalyzerFileFilter(client)
        self.gtp = FortianalyzerGtp(client)
        self.ips = FortianalyzerIps(client)
        self.ssh = FortianalyzerSsh(client)
        self.ssl = FortianalyzerSsl(client)
        self.traffic = FortianalyzerTraffic(client)
        self.virus = FortianalyzerVirus(client)
        self.voip = FortianalyzerVoip(client)
        self.waf = FortianalyzerWaf(client)
        self.webfilter = FortianalyzerWebfilter(client)


class FortianalyzerAnomaly:
    """FortianalyzerAnomaly log operations (type=anomaly)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerAnomaly."""
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
        return self._client.get("log", "/log/fortianalyzer/anomaly/raw", **kwargs)


class FortianalyzerAppCtrl:
    """FortianalyzerAppCtrl log operations (type=app-ctrl)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerAppCtrl."""
        self._client = client
        self.archive = FortianalyzerAppCtrlArchive(client, "app-ctrl")
        self.archive_download = FortianalyzerAppCtrlArchiveDownload(client, "app-ctrl")

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
        return self._client.get("log", "/log/fortianalyzer/app-ctrl/raw", **kwargs)


class FortianalyzerAppCtrlArchive:
    """archive operations for app_ctrl."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize FortianalyzerAppCtrlArchive."""
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
        return self._client.get("log", "/log/fortianalyzer/app-ctrl/archive", **kwargs)


class FortianalyzerAppCtrlArchiveDownload:
    """archive-download operations for app_ctrl."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize FortianalyzerAppCtrlArchiveDownload."""
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
        return self._client.get("log", "/log/fortianalyzer/app-ctrl/archive-download", **kwargs)


class FortianalyzerCifs:
    """FortianalyzerCifs log operations (type=cifs)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerCifs."""
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
        return self._client.get("log", "/log/fortianalyzer/cifs/raw", **kwargs)


class FortianalyzerDlp:
    """FortianalyzerDlp log operations (type=dlp)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerDlp."""
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
        return self._client.get("log", "/log/fortianalyzer/dlp/raw", **kwargs)


class FortianalyzerDns:
    """FortianalyzerDns log operations (type=dns)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerDns."""
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
        return self._client.get("log", "/log/fortianalyzer/dns/raw", **kwargs)


class FortianalyzerEmailfilter:
    """FortianalyzerEmailfilter log operations (type=emailfilter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerEmailfilter."""
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
        return self._client.get("log", "/log/fortianalyzer/emailfilter/raw", **kwargs)


class FortianalyzerEvent:
    """FortianalyzerEvent log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerEvent."""
        self._client = client
        self.compliance_check = FortianalyzerEventComplianceCheck(client, "compliance-check")
        self.connector = FortianalyzerEventConnector(client, "connector")
        self.endpoint = FortianalyzerEventEndpoint(client, "endpoint")
        self.fortiextender = FortianalyzerEventFortiextender(client, "fortiextender")
        self.ha = FortianalyzerEventHa(client, "ha")
        self.router = FortianalyzerEventRouter(client, "router")
        self.security_rating = FortianalyzerEventSecurityRating(client, "security-rating")
        self.system = FortianalyzerEventSystem(client, "system")
        self.user = FortianalyzerEventUser(client, "user")
        self.vpn = FortianalyzerEventVpn(client, "vpn")
        self.wad = FortianalyzerEventWad(client, "wad")
        self.wireless = FortianalyzerEventWireless(client, "wireless")


class FortianalyzerEventComplianceCheck:
    """event logs for compliance-check."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventComplianceCheck."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventConnector:
    """event logs for connector."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventConnector."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventEndpoint:
    """event logs for endpoint."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventEndpoint."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventFortiextender:
    """event logs for fortiextender."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventFortiextender."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventHa:
    """event logs for ha."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventHa."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventRouter:
    """event logs for router."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventRouter."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventSecurityRating:
    """event logs for security-rating."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventSecurityRating."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventSystem:
    """event logs for system."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventSystem."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventUser:
    """event logs for user."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventUser."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventVpn:
    """event logs for vpn."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventVpn."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventWad:
    """event logs for wad."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventWad."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerEventWireless:
    """event logs for wireless."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerEventWireless."""
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
        return self._client.get("log", f"/log/fortianalyzer/event/{self._subtype}/raw", **kwargs)


class FortianalyzerFileFilter:
    """FortianalyzerFileFilter log operations (type=file-filter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerFileFilter."""
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
        return self._client.get("log", "/log/fortianalyzer/file-filter/raw", **kwargs)


class FortianalyzerGtp:
    """FortianalyzerGtp log operations (type=gtp)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerGtp."""
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
        return self._client.get("log", "/log/fortianalyzer/gtp/raw", **kwargs)


class FortianalyzerIps:
    """FortianalyzerIps log operations (type=ips)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerIps."""
        self._client = client
        self.archive = FortianalyzerIpsArchive(client, "ips")
        self.archive_download = FortianalyzerIpsArchiveDownload(client, "ips")

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
        return self._client.get("log", "/log/fortianalyzer/ips/raw", **kwargs)


class FortianalyzerIpsArchive:
    """archive operations for ips."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize FortianalyzerIpsArchive."""
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
        return self._client.get("log", "/log/fortianalyzer/ips/archive", **kwargs)


class FortianalyzerIpsArchiveDownload:
    """archive-download operations for ips."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize FortianalyzerIpsArchiveDownload."""
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
        return self._client.get("log", "/log/fortianalyzer/ips/archive-download", **kwargs)


class FortianalyzerSsh:
    """FortianalyzerSsh log operations (type=ssh)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerSsh."""
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
        return self._client.get("log", "/log/fortianalyzer/ssh/raw", **kwargs)


class FortianalyzerSsl:
    """FortianalyzerSsl log operations (type=ssl)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerSsl."""
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
        return self._client.get("log", "/log/fortianalyzer/ssl/raw", **kwargs)


class FortianalyzerTraffic:
    """FortianalyzerTraffic log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerTraffic."""
        self._client = client
        self.fortiview = FortianalyzerTrafficFortiview(client, "fortiview")
        self.forward = FortianalyzerTrafficForward(client, "forward")
        self.local = FortianalyzerTrafficLocal(client, "local")
        self.multicast = FortianalyzerTrafficMulticast(client, "multicast")
        self.sniffer = FortianalyzerTrafficSniffer(client, "sniffer")
        self.threat = FortianalyzerTrafficThreat(client, "threat")


class FortianalyzerTrafficFortiview:
    """traffic logs for fortiview."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerTrafficFortiview."""
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
        return self._client.get("log", f"/log/fortianalyzer/traffic/{self._subtype}/raw", **kwargs)


class FortianalyzerTrafficForward:
    """traffic logs for forward."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerTrafficForward."""
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
        return self._client.get("log", f"/log/fortianalyzer/traffic/{self._subtype}/raw", **kwargs)


class FortianalyzerTrafficLocal:
    """traffic logs for local."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerTrafficLocal."""
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
        return self._client.get("log", f"/log/fortianalyzer/traffic/{self._subtype}/raw", **kwargs)


class FortianalyzerTrafficMulticast:
    """traffic logs for multicast."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerTrafficMulticast."""
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
        return self._client.get("log", f"/log/fortianalyzer/traffic/{self._subtype}/raw", **kwargs)


class FortianalyzerTrafficSniffer:
    """traffic logs for sniffer."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerTrafficSniffer."""
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
        return self._client.get("log", f"/log/fortianalyzer/traffic/{self._subtype}/raw", **kwargs)


class FortianalyzerTrafficThreat:
    """traffic logs for threat."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize FortianalyzerTrafficThreat."""
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
        return self._client.get("log", f"/log/fortianalyzer/traffic/{self._subtype}/raw", **kwargs)


class FortianalyzerVirus:
    """FortianalyzerVirus log operations (type=virus)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerVirus."""
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
        return self._client.get("log", "/log/fortianalyzer/virus/raw", **kwargs)


class FortianalyzerVoip:
    """FortianalyzerVoip log operations (type=voip)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerVoip."""
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
        return self._client.get("log", "/log/fortianalyzer/voip/raw", **kwargs)


class FortianalyzerWaf:
    """FortianalyzerWaf log operations (type=waf)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerWaf."""
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
        return self._client.get("log", "/log/fortianalyzer/waf/raw", **kwargs)


class FortianalyzerWebfilter:
    """FortianalyzerWebfilter log operations (type=webfilter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize FortianalyzerWebfilter."""
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
        return self._client.get("log", "/log/fortianalyzer/webfilter/raw", **kwargs)
