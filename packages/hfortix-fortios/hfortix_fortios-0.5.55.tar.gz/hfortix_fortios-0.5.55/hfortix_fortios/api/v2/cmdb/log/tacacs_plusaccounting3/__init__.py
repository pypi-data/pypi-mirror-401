"""FortiOS CMDB - TacacsPlusaccounting3 category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Filter",
    "Setting",
    "TacacsPlusaccounting3",
]


class TacacsPlusaccounting3:
    """TacacsPlusaccounting3 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """TacacsPlusaccounting3 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
