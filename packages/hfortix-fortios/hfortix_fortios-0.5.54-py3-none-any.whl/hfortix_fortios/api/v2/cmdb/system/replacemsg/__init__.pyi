"""Type stubs for REPLACEMSG category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .admin import Admin, AdminDictMode, AdminObjectMode
    from .alertmail import Alertmail, AlertmailDictMode, AlertmailObjectMode
    from .auth import Auth, AuthDictMode, AuthObjectMode
    from .automation import Automation, AutomationDictMode, AutomationObjectMode
    from .fortiguard_wf import FortiguardWf, FortiguardWfDictMode, FortiguardWfObjectMode
    from .http import Http, HttpDictMode, HttpObjectMode
    from .mail import Mail, MailDictMode, MailObjectMode
    from .nac_quar import NacQuar, NacQuarDictMode, NacQuarObjectMode
    from .spam import Spam, SpamDictMode, SpamObjectMode
    from .sslvpn import Sslvpn, SslvpnDictMode, SslvpnObjectMode
    from .traffic_quota import TrafficQuota, TrafficQuotaDictMode, TrafficQuotaObjectMode
    from .utm import Utm, UtmDictMode, UtmObjectMode

__all__ = [
    "Admin",
    "Alertmail",
    "Auth",
    "Automation",
    "FortiguardWf",
    "Http",
    "Mail",
    "NacQuar",
    "Spam",
    "Sslvpn",
    "TrafficQuota",
    "Utm",
    "ReplacemsgDictMode",
    "ReplacemsgObjectMode",
]

class ReplacemsgDictMode:
    """REPLACEMSG API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    admin: AdminDictMode
    alertmail: AlertmailDictMode
    auth: AuthDictMode
    automation: AutomationDictMode
    fortiguard_wf: FortiguardWfDictMode
    http: HttpDictMode
    mail: MailDictMode
    nac_quar: NacQuarDictMode
    spam: SpamDictMode
    sslvpn: SslvpnDictMode
    traffic_quota: TrafficQuotaDictMode
    utm: UtmDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize replacemsg category with HTTP client."""
        ...


class ReplacemsgObjectMode:
    """REPLACEMSG API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    admin: AdminObjectMode
    alertmail: AlertmailObjectMode
    auth: AuthObjectMode
    automation: AutomationObjectMode
    fortiguard_wf: FortiguardWfObjectMode
    http: HttpObjectMode
    mail: MailObjectMode
    nac_quar: NacQuarObjectMode
    spam: SpamObjectMode
    sslvpn: SslvpnObjectMode
    traffic_quota: TrafficQuotaObjectMode
    utm: UtmObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize replacemsg category with HTTP client."""
        ...


# Base class for backwards compatibility
class Replacemsg:
    """REPLACEMSG API category."""
    
    admin: Admin
    alertmail: Alertmail
    auth: Auth
    automation: Automation
    fortiguard_wf: FortiguardWf
    http: Http
    mail: Mail
    nac_quar: NacQuar
    spam: Spam
    sslvpn: Sslvpn
    traffic_quota: TrafficQuota
    utm: Utm

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize replacemsg category with HTTP client."""
        ...
