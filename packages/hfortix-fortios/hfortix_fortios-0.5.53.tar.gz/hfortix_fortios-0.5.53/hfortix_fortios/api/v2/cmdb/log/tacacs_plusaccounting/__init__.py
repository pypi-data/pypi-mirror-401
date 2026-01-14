"""FortiOS CMDB - TacacsPlusaccounting category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Filter",
    "Setting",
    "TacacsPlusaccounting",
]


class TacacsPlusaccounting:
    """TacacsPlusaccounting endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """TacacsPlusaccounting endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
