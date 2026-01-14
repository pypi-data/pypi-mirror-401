"""
FortiOS LOG API - Forticloud

Log query endpoints for forticloud logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They accept path parameters that are represented as nested classes.

Example Usage:
    >>> fgt.api.log.forticloud.event.vpn.get(rows=100)
    >>> fgt.api.log.forticloud.traffic.forward.get(rows=50)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from hfortix_core.http.interface import IHTTPClient


class Forticloud:
    """Forticloud log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize Forticloud endpoint."""
        self._client = client
        self.anomaly = ForticloudAnomaly(client)
        self.app_ctrl = ForticloudAppCtrl(client)
        self.cifs = ForticloudCifs(client)
        self.dlp = ForticloudDlp(client)
        self.dns = ForticloudDns(client)
        self.emailfilter = ForticloudEmailfilter(client)
        self.event = ForticloudEvent(client)
        self.file_filter = ForticloudFileFilter(client)
        self.gtp = ForticloudGtp(client)
        self.ips = ForticloudIps(client)
        self.ssh = ForticloudSsh(client)
        self.ssl = ForticloudSsl(client)
        self.traffic = ForticloudTraffic(client)
        self.virus = ForticloudVirus(client)
        self.voip = ForticloudVoip(client)
        self.waf = ForticloudWaf(client)
        self.webfilter = ForticloudWebfilter(client)


class ForticloudAnomaly:
    """ForticloudAnomaly log operations (type=anomaly)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudAnomaly."""
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
        return self._client.get("log", "/log/forticloud/anomaly/raw", **kwargs)


class ForticloudAppCtrl:
    """ForticloudAppCtrl log operations (type=app-ctrl)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudAppCtrl."""
        self._client = client
        self.archive = ForticloudAppCtrlArchive(client, "app-ctrl")
        self.archive_download = ForticloudAppCtrlArchiveDownload(client, "app-ctrl")

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
        return self._client.get("log", "/log/forticloud/app-ctrl/raw", **kwargs)


class ForticloudAppCtrlArchive:
    """archive operations for app_ctrl."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize ForticloudAppCtrlArchive."""
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
        return self._client.get("log", "/log/forticloud/app-ctrl/archive", **kwargs)


class ForticloudAppCtrlArchiveDownload:
    """archive-download operations for app_ctrl."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize ForticloudAppCtrlArchiveDownload."""
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
        return self._client.get("log", "/log/forticloud/app-ctrl/archive-download", **kwargs)


class ForticloudCifs:
    """ForticloudCifs log operations (type=cifs)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudCifs."""
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
        return self._client.get("log", "/log/forticloud/cifs/raw", **kwargs)


class ForticloudDlp:
    """ForticloudDlp log operations (type=dlp)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudDlp."""
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
        return self._client.get("log", "/log/forticloud/dlp/raw", **kwargs)


class ForticloudDns:
    """ForticloudDns log operations (type=dns)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudDns."""
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
        return self._client.get("log", "/log/forticloud/dns/raw", **kwargs)


class ForticloudEmailfilter:
    """ForticloudEmailfilter log operations (type=emailfilter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEmailfilter."""
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
        return self._client.get("log", "/log/forticloud/emailfilter/raw", **kwargs)


class ForticloudEvent:
    """ForticloudEvent log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEvent."""
        self._client = client
        self.compliance_check = ForticloudEventComplianceCheck(client, "compliance-check")
        self.connector = ForticloudEventConnector(client, "connector")
        self.endpoint = ForticloudEventEndpoint(client, "endpoint")
        self.fortiextender = ForticloudEventFortiextender(client, "fortiextender")
        self.ha = ForticloudEventHa(client, "ha")
        self.router = ForticloudEventRouter(client, "router")
        self.security_rating = ForticloudEventSecurityRating(client, "security-rating")
        self.system = ForticloudEventSystem(client, "system")
        self.user = ForticloudEventUser(client, "user")
        self.vpn = ForticloudEventVpn(client, "vpn")
        self.wad = ForticloudEventWad(client, "wad")
        self.wireless = ForticloudEventWireless(client, "wireless")


class ForticloudEventComplianceCheck:
    """event logs for compliance-check."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventComplianceCheck."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventConnector:
    """event logs for connector."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventConnector."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventEndpoint:
    """event logs for endpoint."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventEndpoint."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventFortiextender:
    """event logs for fortiextender."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventFortiextender."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventHa:
    """event logs for ha."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventHa."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventRouter:
    """event logs for router."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventRouter."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventSecurityRating:
    """event logs for security-rating."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventSecurityRating."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventSystem:
    """event logs for system."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventSystem."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventUser:
    """event logs for user."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventUser."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventVpn:
    """event logs for vpn."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventVpn."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventWad:
    """event logs for wad."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventWad."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudEventWireless:
    """event logs for wireless."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudEventWireless."""
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
        return self._client.get("log", f"/log/forticloud/event/{self._subtype}/raw", **kwargs)


class ForticloudFileFilter:
    """ForticloudFileFilter log operations (type=file-filter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudFileFilter."""
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
        return self._client.get("log", "/log/forticloud/file-filter/raw", **kwargs)


class ForticloudGtp:
    """ForticloudGtp log operations (type=gtp)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudGtp."""
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
        return self._client.get("log", "/log/forticloud/gtp/raw", **kwargs)


class ForticloudIps:
    """ForticloudIps log operations (type=ips)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudIps."""
        self._client = client
        self.archive = ForticloudIpsArchive(client, "ips")
        self.archive_download = ForticloudIpsArchiveDownload(client, "ips")

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
        return self._client.get("log", "/log/forticloud/ips/raw", **kwargs)


class ForticloudIpsArchive:
    """archive operations for ips."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize ForticloudIpsArchive."""
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
        return self._client.get("log", "/log/forticloud/ips/archive", **kwargs)


class ForticloudIpsArchiveDownload:
    """archive-download operations for ips."""

    def __init__(self, client: "IHTTPClient", type_value: str):
        """Initialize ForticloudIpsArchiveDownload."""
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
        return self._client.get("log", "/log/forticloud/ips/archive-download", **kwargs)


class ForticloudSsh:
    """ForticloudSsh log operations (type=ssh)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudSsh."""
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
        return self._client.get("log", "/log/forticloud/ssh/raw", **kwargs)


class ForticloudSsl:
    """ForticloudSsl log operations (type=ssl)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudSsl."""
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
        return self._client.get("log", "/log/forticloud/ssl/raw", **kwargs)


class ForticloudTraffic:
    """ForticloudTraffic log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTraffic."""
        self._client = client
        self.fortiview = ForticloudTrafficFortiview(client, "fortiview")
        self.forward = ForticloudTrafficForward(client, "forward")
        self.local = ForticloudTrafficLocal(client, "local")
        self.multicast = ForticloudTrafficMulticast(client, "multicast")
        self.sniffer = ForticloudTrafficSniffer(client, "sniffer")
        self.threat = ForticloudTrafficThreat(client, "threat")


class ForticloudTrafficFortiview:
    """traffic logs for fortiview."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudTrafficFortiview."""
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
        return self._client.get("log", f"/log/forticloud/traffic/{self._subtype}/raw", **kwargs)


class ForticloudTrafficForward:
    """traffic logs for forward."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudTrafficForward."""
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
        return self._client.get("log", f"/log/forticloud/traffic/{self._subtype}/raw", **kwargs)


class ForticloudTrafficLocal:
    """traffic logs for local."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudTrafficLocal."""
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
        return self._client.get("log", f"/log/forticloud/traffic/{self._subtype}/raw", **kwargs)


class ForticloudTrafficMulticast:
    """traffic logs for multicast."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudTrafficMulticast."""
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
        return self._client.get("log", f"/log/forticloud/traffic/{self._subtype}/raw", **kwargs)


class ForticloudTrafficSniffer:
    """traffic logs for sniffer."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudTrafficSniffer."""
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
        return self._client.get("log", f"/log/forticloud/traffic/{self._subtype}/raw", **kwargs)


class ForticloudTrafficThreat:
    """traffic logs for threat."""

    def __init__(self, client: "IHTTPClient", subtype: str):
        """Initialize ForticloudTrafficThreat."""
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
        return self._client.get("log", f"/log/forticloud/traffic/{self._subtype}/raw", **kwargs)


class ForticloudVirus:
    """ForticloudVirus log operations (type=virus)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudVirus."""
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
        return self._client.get("log", "/log/forticloud/virus/raw", **kwargs)


class ForticloudVoip:
    """ForticloudVoip log operations (type=voip)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudVoip."""
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
        return self._client.get("log", "/log/forticloud/voip/raw", **kwargs)


class ForticloudWaf:
    """ForticloudWaf log operations (type=waf)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudWaf."""
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
        return self._client.get("log", "/log/forticloud/waf/raw", **kwargs)


class ForticloudWebfilter:
    """ForticloudWebfilter log operations (type=webfilter)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudWebfilter."""
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
        return self._client.get("log", "/log/forticloud/webfilter/raw", **kwargs)
