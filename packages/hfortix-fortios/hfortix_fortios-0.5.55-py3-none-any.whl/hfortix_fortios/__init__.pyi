"""Type stubs for FortiOS API v2."""

from .client import FortiOS as FortiOS
from .client import FortiOSDictMode as FortiOSDictMode
from .client import FortiOSObjectMode as FortiOSObjectMode
from .cmdb import CMDB as CMDB
from .log import Log as Log
from .monitor import Monitor as Monitor
from .service import Service as Service

__all__ = [
    "FortiOS",
    "FortiOSDictMode",
    "FortiOSObjectMode",
    "CMDB",
    "Monitor",
    "Service",
    "Log",
]
