"""Type stubs for DLP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .data_type import DataType, DataTypeDictMode, DataTypeObjectMode
    from .dictionary import Dictionary, DictionaryDictMode, DictionaryObjectMode
    from .exact_data_match import ExactDataMatch, ExactDataMatchDictMode, ExactDataMatchObjectMode
    from .filepattern import Filepattern, FilepatternDictMode, FilepatternObjectMode
    from .label import Label, LabelDictMode, LabelObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode
    from .sensor import Sensor, SensorDictMode, SensorObjectMode
    from .settings import Settings, SettingsDictMode, SettingsObjectMode

__all__ = [
    "DataType",
    "Dictionary",
    "ExactDataMatch",
    "Filepattern",
    "Label",
    "Profile",
    "Sensor",
    "Settings",
    "DlpDictMode",
    "DlpObjectMode",
]

class DlpDictMode:
    """DLP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    data_type: DataTypeDictMode
    dictionary: DictionaryDictMode
    exact_data_match: ExactDataMatchDictMode
    filepattern: FilepatternDictMode
    label: LabelDictMode
    profile: ProfileDictMode
    sensor: SensorDictMode
    settings: SettingsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dlp category with HTTP client."""
        ...


class DlpObjectMode:
    """DLP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    data_type: DataTypeObjectMode
    dictionary: DictionaryObjectMode
    exact_data_match: ExactDataMatchObjectMode
    filepattern: FilepatternObjectMode
    label: LabelObjectMode
    profile: ProfileObjectMode
    sensor: SensorObjectMode
    settings: SettingsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dlp category with HTTP client."""
        ...


# Base class for backwards compatibility
class Dlp:
    """DLP API category."""
    
    data_type: DataType
    dictionary: Dictionary
    exact_data_match: ExactDataMatch
    filepattern: Filepattern
    label: Label
    profile: Profile
    sensor: Sensor
    settings: Settings

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dlp category with HTTP client."""
        ...
