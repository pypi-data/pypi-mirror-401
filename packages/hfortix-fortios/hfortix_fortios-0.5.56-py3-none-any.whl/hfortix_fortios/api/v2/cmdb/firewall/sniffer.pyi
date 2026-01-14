from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class SnifferPayload(TypedDict, total=False):
    """
    Type hints for firewall/sniffer payload fields.
    
    Configure sniffer.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.antivirus.profile.ProfileEndpoint` (via: av-profile)
        - :class:`~.application.list.ListEndpoint` (via: application-list)
        - :class:`~.dlp.profile.ProfileEndpoint` (via: dlp-profile)
        - :class:`~.emailfilter.profile.ProfileEndpoint` (via: emailfilter-profile)
        - :class:`~.file-filter.profile.ProfileEndpoint` (via: file-filter-profile)
        - :class:`~.ips.sensor.SensorEndpoint` (via: ips-sensor)
        - :class:`~.system.interface.InterfaceEndpoint` (via: interface)
        - :class:`~.webfilter.profile.ProfileEndpoint` (via: webfilter-profile)

    **Usage:**
        payload: SnifferPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    id: int  # Sniffer ID (0 - 9999). | Default: 0 | Min: 0 | Max: 9999
    uuid: str  # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    status: Literal["enable", "disable"]  # Enable/disable the active status of the sniffer. | Default: enable
    logtraffic: Literal["all", "utm", "disable"]  # Either log all sessions, only sessions that have a | Default: utm
    ipv6: Literal["enable", "disable"]  # Enable/disable sniffing IPv6 packets. | Default: disable
    non_ip: Literal["enable", "disable"]  # Enable/disable sniffing non-IP packets. | Default: disable
    interface: str  # Interface name that traffic sniffing will take pla | MaxLen: 35
    host: str  # Hosts to filter for in sniffer traffic | MaxLen: 63
    port: str  # Ports to sniff | MaxLen: 63
    protocol: str  # Integer value for the protocol type as defined by | MaxLen: 63
    vlan: str  # List of VLANs to sniff. | MaxLen: 63
    application_list_status: Literal["enable", "disable"]  # Enable/disable application control profile. | Default: disable
    application_list: str  # Name of an existing application list. | MaxLen: 47
    ips_sensor_status: Literal["enable", "disable"]  # Enable/disable IPS sensor. | Default: disable
    ips_sensor: str  # Name of an existing IPS sensor. | MaxLen: 47
    dsri: Literal["enable", "disable"]  # Enable/disable DSRI. | Default: disable
    av_profile_status: Literal["enable", "disable"]  # Enable/disable antivirus profile. | Default: disable
    av_profile: str  # Name of an existing antivirus profile. | MaxLen: 47
    webfilter_profile_status: Literal["enable", "disable"]  # Enable/disable web filter profile. | Default: disable
    webfilter_profile: str  # Name of an existing web filter profile. | MaxLen: 47
    emailfilter_profile_status: Literal["enable", "disable"]  # Enable/disable emailfilter. | Default: disable
    emailfilter_profile: str  # Name of an existing email filter profile. | MaxLen: 47
    dlp_profile_status: Literal["enable", "disable"]  # Enable/disable DLP profile. | Default: disable
    dlp_profile: str  # Name of an existing DLP profile. | MaxLen: 47
    ip_threatfeed_status: Literal["enable", "disable"]  # Enable/disable IP threat feed. | Default: disable
    ip_threatfeed: list[dict[str, Any]]  # Name of an existing IP threat feed.
    file_filter_profile_status: Literal["enable", "disable"]  # Enable/disable file filter. | Default: disable
    file_filter_profile: str  # Name of an existing file-filter profile. | MaxLen: 47
    ips_dos_status: Literal["enable", "disable"]  # Enable/disable IPS DoS anomaly detection. | Default: disable
    anomaly: list[dict[str, Any]]  # Configuration method to edit Denial of Service

# Nested TypedDicts for table field children (dict mode)

class SnifferIpthreatfeedItem(TypedDict):
    """Type hints for ip-threatfeed table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Threat feed name. | MaxLen: 79


class SnifferAnomalyItem(TypedDict):
    """Type hints for anomaly table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Anomaly name. | MaxLen: 63
    status: Literal["disable", "enable"]  # Enable/disable this anomaly. | Default: disable
    log: Literal["enable", "disable"]  # Enable/disable anomaly logging. | Default: disable
    action: Literal["pass", "block"]  # Action taken when the threshold is reached. | Default: pass
    quarantine: Literal["none", "attacker"]  # Quarantine method. | Default: none
    quarantine_expiry: str  # Duration of quarantine. | Default: 5m
    quarantine_log: Literal["disable", "enable"]  # Enable/disable quarantine logging. | Default: enable
    threshold: int  # Anomaly threshold. Number of detected instances | Default: 0 | Min: 1 | Max: 2147483647
    threshold(default): int  # Number of detected instances | Default: 0 | Min: 0 | Max: 4294967295


# Nested classes for table field children (object mode)

@final
class SnifferIpthreatfeedObject:
    """Typed object for ip-threatfeed table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Threat feed name. | MaxLen: 79
    name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class SnifferAnomalyObject:
    """Typed object for anomaly table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Anomaly name. | MaxLen: 63
    name: str
    # Enable/disable this anomaly. | Default: disable
    status: Literal["disable", "enable"]
    # Enable/disable anomaly logging. | Default: disable
    log: Literal["enable", "disable"]
    # Action taken when the threshold is reached. | Default: pass
    action: Literal["pass", "block"]
    # Quarantine method. | Default: none
    quarantine: Literal["none", "attacker"]
    # Duration of quarantine. | Default: 5m
    quarantine_expiry: str
    # Enable/disable quarantine logging. | Default: enable
    quarantine_log: Literal["disable", "enable"]
    # Anomaly threshold. Number of detected instances | Default: 0 | Min: 1 | Max: 2147483647
    threshold: int
    # Number of detected instances | Default: 0 | Min: 0 | Max: 4294967295
    threshold(default): int
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class SnifferResponse(TypedDict):
    """
    Type hints for firewall/sniffer API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    id: int  # Sniffer ID (0 - 9999). | Default: 0 | Min: 0 | Max: 9999
    uuid: str  # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    status: Literal["enable", "disable"]  # Enable/disable the active status of the sniffer. | Default: enable
    logtraffic: Literal["all", "utm", "disable"]  # Either log all sessions, only sessions that have a | Default: utm
    ipv6: Literal["enable", "disable"]  # Enable/disable sniffing IPv6 packets. | Default: disable
    non_ip: Literal["enable", "disable"]  # Enable/disable sniffing non-IP packets. | Default: disable
    interface: str  # Interface name that traffic sniffing will take pla | MaxLen: 35
    host: str  # Hosts to filter for in sniffer traffic | MaxLen: 63
    port: str  # Ports to sniff | MaxLen: 63
    protocol: str  # Integer value for the protocol type as defined by | MaxLen: 63
    vlan: str  # List of VLANs to sniff. | MaxLen: 63
    application_list_status: Literal["enable", "disable"]  # Enable/disable application control profile. | Default: disable
    application_list: str  # Name of an existing application list. | MaxLen: 47
    ips_sensor_status: Literal["enable", "disable"]  # Enable/disable IPS sensor. | Default: disable
    ips_sensor: str  # Name of an existing IPS sensor. | MaxLen: 47
    dsri: Literal["enable", "disable"]  # Enable/disable DSRI. | Default: disable
    av_profile_status: Literal["enable", "disable"]  # Enable/disable antivirus profile. | Default: disable
    av_profile: str  # Name of an existing antivirus profile. | MaxLen: 47
    webfilter_profile_status: Literal["enable", "disable"]  # Enable/disable web filter profile. | Default: disable
    webfilter_profile: str  # Name of an existing web filter profile. | MaxLen: 47
    emailfilter_profile_status: Literal["enable", "disable"]  # Enable/disable emailfilter. | Default: disable
    emailfilter_profile: str  # Name of an existing email filter profile. | MaxLen: 47
    dlp_profile_status: Literal["enable", "disable"]  # Enable/disable DLP profile. | Default: disable
    dlp_profile: str  # Name of an existing DLP profile. | MaxLen: 47
    ip_threatfeed_status: Literal["enable", "disable"]  # Enable/disable IP threat feed. | Default: disable
    ip_threatfeed: list[SnifferIpthreatfeedItem]  # Name of an existing IP threat feed.
    file_filter_profile_status: Literal["enable", "disable"]  # Enable/disable file filter. | Default: disable
    file_filter_profile: str  # Name of an existing file-filter profile. | MaxLen: 47
    ips_dos_status: Literal["enable", "disable"]  # Enable/disable IPS DoS anomaly detection. | Default: disable
    anomaly: list[SnifferAnomalyItem]  # Configuration method to edit Denial of Service


@final
class SnifferObject:
    """Typed FortiObject for firewall/sniffer with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Sniffer ID (0 - 9999). | Default: 0 | Min: 0 | Max: 9999
    id: int
    # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    uuid: str
    # Enable/disable the active status of the sniffer. | Default: enable
    status: Literal["enable", "disable"]
    # Either log all sessions, only sessions that have a security | Default: utm
    logtraffic: Literal["all", "utm", "disable"]
    # Enable/disable sniffing IPv6 packets. | Default: disable
    ipv6: Literal["enable", "disable"]
    # Enable/disable sniffing non-IP packets. | Default: disable
    non_ip: Literal["enable", "disable"]
    # Interface name that traffic sniffing will take place on. | MaxLen: 35
    interface: str
    # Hosts to filter for in sniffer traffic | MaxLen: 63
    host: str
    # Ports to sniff | MaxLen: 63
    port: str
    # Integer value for the protocol type as defined by IANA | MaxLen: 63
    protocol: str
    # List of VLANs to sniff. | MaxLen: 63
    vlan: str
    # Enable/disable application control profile. | Default: disable
    application_list_status: Literal["enable", "disable"]
    # Name of an existing application list. | MaxLen: 47
    application_list: str
    # Enable/disable IPS sensor. | Default: disable
    ips_sensor_status: Literal["enable", "disable"]
    # Name of an existing IPS sensor. | MaxLen: 47
    ips_sensor: str
    # Enable/disable DSRI. | Default: disable
    dsri: Literal["enable", "disable"]
    # Enable/disable antivirus profile. | Default: disable
    av_profile_status: Literal["enable", "disable"]
    # Name of an existing antivirus profile. | MaxLen: 47
    av_profile: str
    # Enable/disable web filter profile. | Default: disable
    webfilter_profile_status: Literal["enable", "disable"]
    # Name of an existing web filter profile. | MaxLen: 47
    webfilter_profile: str
    # Enable/disable emailfilter. | Default: disable
    emailfilter_profile_status: Literal["enable", "disable"]
    # Name of an existing email filter profile. | MaxLen: 47
    emailfilter_profile: str
    # Enable/disable DLP profile. | Default: disable
    dlp_profile_status: Literal["enable", "disable"]
    # Name of an existing DLP profile. | MaxLen: 47
    dlp_profile: str
    # Enable/disable IP threat feed. | Default: disable
    ip_threatfeed_status: Literal["enable", "disable"]
    # Name of an existing IP threat feed.
    ip_threatfeed: list[SnifferIpthreatfeedObject]
    # Enable/disable file filter. | Default: disable
    file_filter_profile_status: Literal["enable", "disable"]
    # Name of an existing file-filter profile. | MaxLen: 47
    file_filter_profile: str
    # Enable/disable IPS DoS anomaly detection. | Default: disable
    ips_dos_status: Literal["enable", "disable"]
    # Configuration method to edit Denial of Service (DoS) anomaly
    anomaly: list[SnifferAnomalyObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> SnifferPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Sniffer:
    """
    Configure sniffer.
    
    Path: firewall/sniffer
    Category: cmdb
    Primary Key: id
    """
    
    # ================================================================
    # DEFAULT MODE OVERLOADS (no response_mode) - MUST BE FIRST
    # These match when response_mode is NOT passed (client default is "dict")
    # Pylance matches overloads top-to-bottom, so these must come first!
    # ================================================================
    
    # Default mode: mkey as positional arg -> returns typed dict
    @overload
    def get(
        self,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> SnifferResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> SnifferResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        id: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[SnifferResponse]: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # Object mode: no mkey -> returns list of objects
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> list[SnifferObject]: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        id: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        response_mode: Literal["object"] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Dict mode with mkey provided as positional arg (single dict)
    @overload
    def get(
        self,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> SnifferResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> SnifferResponse: ...
    
    # Dict mode - list of dicts (no mkey/name provided) - keyword-only signature
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> list[SnifferResponse]: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        id: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> Union[dict[str, Any], list[dict[str, Any]], FortiObject, list[FortiObject]]: ...
    
    def get(
        self,
        id: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: str | None = ...,
        **kwargs: Any,
    ) -> SnifferObject | list[SnifferObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # Helper methods
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> Union[list[str], list[dict[str, Any]]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> dict[str, Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> dict[str, Any]: ...
    
    @staticmethod
    def schema() -> dict[str, Any]: ...


# ================================================================
# MODE-SPECIFIC CLASSES FOR CLIENT-LEVEL response_mode SUPPORT
# ================================================================

class SnifferDictMode:
    """Sniffer endpoint for dict response mode (default for this client).
    
    By default returns SnifferResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return SnifferObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        id: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Object mode override with mkey (single item)
    @overload
    def get(
        self,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        id: None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> list[SnifferObject]: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> SnifferResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        id: None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> list[SnifferResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> Union[list[str], list[dict[str, Any]]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> dict[str, Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> dict[str, Any]: ...
    
    @staticmethod
    def schema() -> dict[str, Any]: ...


class SnifferObjectMode:
    """Sniffer endpoint for object response mode (default for this client).
    
    By default returns SnifferObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return SnifferResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        id: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Dict mode override with mkey (single item)
    @overload
    def get(
        self,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> SnifferResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        id: None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> list[SnifferResponse]: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["object"] | None = ...,
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        id: None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["object"] | None = ...,
        **kwargs: Any,
    ) -> list[SnifferObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SnifferObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SnifferPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        non_ip: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        host: str | None = ...,
        port: str | None = ...,
        protocol: str | None = ...,
        vlan: str | None = ...,
        application_list_status: Literal["enable", "disable"] | None = ...,
        application_list: str | None = ...,
        ips_sensor_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        dsri: Literal["enable", "disable"] | None = ...,
        av_profile_status: Literal["enable", "disable"] | None = ...,
        av_profile: str | None = ...,
        webfilter_profile_status: Literal["enable", "disable"] | None = ...,
        webfilter_profile: str | None = ...,
        emailfilter_profile_status: Literal["enable", "disable"] | None = ...,
        emailfilter_profile: str | None = ...,
        dlp_profile_status: Literal["enable", "disable"] | None = ...,
        dlp_profile: str | None = ...,
        ip_threatfeed_status: Literal["enable", "disable"] | None = ...,
        ip_threatfeed: str | list[str] | list[dict[str, Any]] | None = ...,
        file_filter_profile_status: Literal["enable", "disable"] | None = ...,
        file_filter_profile: str | None = ...,
        ips_dos_status: Literal["enable", "disable"] | None = ...,
        anomaly: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> Union[list[str], list[dict[str, Any]]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> dict[str, Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> dict[str, Any]: ...
    
    @staticmethod
    def schema() -> dict[str, Any]: ...


__all__ = [
    "Sniffer",
    "SnifferDictMode",
    "SnifferObjectMode",
    "SnifferPayload",
    "SnifferObject",
]