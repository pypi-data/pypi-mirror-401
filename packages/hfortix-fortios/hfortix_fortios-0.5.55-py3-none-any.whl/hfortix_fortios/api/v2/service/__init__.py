"""FortiOS CMDB - Service category"""

from . import security_rating
from . import sniffer
from . import system

__all__ = [
    "SecurityRating",
    "Service",
    "Sniffer",
    "System",
]


class Service:
    """Service endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Service endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.security_rating = security_rating.SecurityRating(client)
        self.sniffer = sniffer.Sniffer(client)
        self.system = system.System(client)
