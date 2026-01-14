"""Type stubs for IPS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .custom import Custom, CustomDictMode, CustomObjectMode
    from .decoder import Decoder, DecoderDictMode, DecoderObjectMode
    from .global_ import Global, GlobalDictMode, GlobalObjectMode
    from .rule import Rule, RuleDictMode, RuleObjectMode
    from .rule_settings import RuleSettings, RuleSettingsDictMode, RuleSettingsObjectMode
    from .sensor import Sensor, SensorDictMode, SensorObjectMode
    from .settings import Settings, SettingsDictMode, SettingsObjectMode
    from .view_map import ViewMap, ViewMapDictMode, ViewMapObjectMode

__all__ = [
    "Custom",
    "Decoder",
    "Global",
    "Rule",
    "RuleSettings",
    "Sensor",
    "Settings",
    "ViewMap",
    "IpsDictMode",
    "IpsObjectMode",
]

class IpsDictMode:
    """IPS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    custom: CustomDictMode
    decoder: DecoderDictMode
    global_: GlobalDictMode
    rule: RuleDictMode
    rule_settings: RuleSettingsDictMode
    sensor: SensorDictMode
    settings: SettingsDictMode
    view_map: ViewMapDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ips category with HTTP client."""
        ...


class IpsObjectMode:
    """IPS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    custom: CustomObjectMode
    decoder: DecoderObjectMode
    global_: GlobalObjectMode
    rule: RuleObjectMode
    rule_settings: RuleSettingsObjectMode
    sensor: SensorObjectMode
    settings: SettingsObjectMode
    view_map: ViewMapObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ips category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ips:
    """IPS API category."""
    
    custom: Custom
    decoder: Decoder
    global_: Global
    rule: Rule
    rule_settings: RuleSettings
    sensor: Sensor
    settings: Settings
    view_map: ViewMap

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ips category with HTTP client."""
        ...
