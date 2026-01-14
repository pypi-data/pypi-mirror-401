"""Type stubs for LICENSE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .fortianalyzer_status import FortianalyzerStatus, FortianalyzerStatusDictMode, FortianalyzerStatusObjectMode
    from .forticare_org_list import ForticareOrgList, ForticareOrgListDictMode, ForticareOrgListObjectMode
    from .forticare_resellers import ForticareResellers, ForticareResellersDictMode, ForticareResellersObjectMode
    from .status import Status, StatusDictMode, StatusObjectMode
    from .database import DatabaseDictMode, DatabaseObjectMode

__all__ = [
    "FortianalyzerStatus",
    "ForticareOrgList",
    "ForticareResellers",
    "Status",
    "LicenseDictMode",
    "LicenseObjectMode",
]

class LicenseDictMode:
    """LICENSE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    database: DatabaseDictMode
    fortianalyzer_status: FortianalyzerStatusDictMode
    forticare_org_list: ForticareOrgListDictMode
    forticare_resellers: ForticareResellersDictMode
    status: StatusDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize license category with HTTP client."""
        ...


class LicenseObjectMode:
    """LICENSE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    database: DatabaseObjectMode
    fortianalyzer_status: FortianalyzerStatusObjectMode
    forticare_org_list: ForticareOrgListObjectMode
    forticare_resellers: ForticareResellersObjectMode
    status: StatusObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize license category with HTTP client."""
        ...


# Base class for backwards compatibility
class License:
    """LICENSE API category."""
    
    database: Database
    fortianalyzer_status: FortianalyzerStatus
    forticare_org_list: ForticareOrgList
    forticare_resellers: ForticareResellers
    status: Status

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize license category with HTTP client."""
        ...
