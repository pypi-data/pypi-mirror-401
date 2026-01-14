"""FortiOS CMDB - TacacsPlusaccounting2 category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Filter",
    "Setting",
    "TacacsPlusaccounting2",
]


class TacacsPlusaccounting2:
    """TacacsPlusaccounting2 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """TacacsPlusaccounting2 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
