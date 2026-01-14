from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class TimersPayload(TypedDict, total=False):
    """
    Type hints for wireless_controller/timers payload fields.
    
    Configure CAPWAP timers.
    
    **Usage:**
        payload: TimersPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    echo_interval: int  # Time between echo requests sent by the managed WTP | Default: 30 | Min: 1 | Max: 255
    nat_session_keep_alive: int  # Maximal time in seconds between control requests s | Default: 0 | Min: 0 | Max: 255
    discovery_interval: int  # Time between discovery requests | Default: 5 | Min: 2 | Max: 180
    client_idle_timeout: int  # Time after which a client is considered idle and t | Default: 300 | Min: 20 | Max: 3600
    client_idle_rehome_timeout: int  # Time after which a client is considered idle and d | Default: 20 | Min: 2 | Max: 3600
    auth_timeout: int  # Time after which a client is considered failed in | Default: 5 | Min: 5 | Max: 30
    rogue_ap_log: int  # Time between logging rogue AP messages if periodic | Default: 0 | Min: 0 | Max: 1440
    fake_ap_log: int  # Time between recording logs about fake APs if peri | Default: 1 | Min: 1 | Max: 1440
    sta_offline_cleanup: int  # Time period in seconds to keep station offline dat | Default: 300 | Min: 0 | Max: 4294967295
    sta_offline_ip2mac_cleanup: int  # Time period in seconds to keep station offline Ip2 | Default: 300 | Min: 0 | Max: 4294967295
    sta_cap_cleanup: int  # Time period in minutes to keep station capability | Default: 0 | Min: 0 | Max: 4294967295
    rogue_ap_cleanup: int  # Time period in minutes to keep rogue AP after it i | Default: 0 | Min: 0 | Max: 4294967295
    rogue_sta_cleanup: int  # Time period in minutes to keep rogue station after | Default: 0 | Min: 0 | Max: 4294967295
    wids_entry_cleanup: int  # Time period in minutes to keep wids entry after it | Default: 0 | Min: 0 | Max: 4294967295
    ble_device_cleanup: int  # Time period in minutes to keep BLE device after it | Default: 60 | Min: 0 | Max: 4294967295
    sta_stats_interval: int  # Time between running client (station) reports | Default: 10 | Min: 1 | Max: 255
    vap_stats_interval: int  # Time between running Virtual Access Point (VAP) re | Default: 15 | Min: 1 | Max: 255
    radio_stats_interval: int  # Time between running radio reports | Default: 15 | Min: 1 | Max: 255
    sta_capability_interval: int  # Time between running station capability reports | Default: 30 | Min: 1 | Max: 255
    sta_locate_timer: int  # Time between running client presence flushes to re | Default: 1800 | Min: 0 | Max: 86400
    ipsec_intf_cleanup: int  # Time period to keep IPsec VPN interfaces up after | Default: 120 | Min: 30 | Max: 3600
    ble_scan_report_intv: int  # Time between running Bluetooth Low Energy (BLE) re | Default: 30 | Min: 10 | Max: 3600
    drma_interval: int  # Dynamic radio mode assignment (DRMA) schedule inte | Default: 60 | Min: 1 | Max: 1440
    ap_reboot_wait_interval1: int  # Time in minutes to wait before AP reboots when the | Default: 0 | Min: 5 | Max: 65535
    ap_reboot_wait_time: str  # Time to reboot the AP when there is no controller | MaxLen: 7
    ap_reboot_wait_interval2: int  # Time in minutes to wait before AP reboots when the | Default: 0 | Min: 5 | Max: 65535

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class TimersResponse(TypedDict):
    """
    Type hints for wireless_controller/timers API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    echo_interval: int  # Time between echo requests sent by the managed WTP | Default: 30 | Min: 1 | Max: 255
    nat_session_keep_alive: int  # Maximal time in seconds between control requests s | Default: 0 | Min: 0 | Max: 255
    discovery_interval: int  # Time between discovery requests | Default: 5 | Min: 2 | Max: 180
    client_idle_timeout: int  # Time after which a client is considered idle and t | Default: 300 | Min: 20 | Max: 3600
    client_idle_rehome_timeout: int  # Time after which a client is considered idle and d | Default: 20 | Min: 2 | Max: 3600
    auth_timeout: int  # Time after which a client is considered failed in | Default: 5 | Min: 5 | Max: 30
    rogue_ap_log: int  # Time between logging rogue AP messages if periodic | Default: 0 | Min: 0 | Max: 1440
    fake_ap_log: int  # Time between recording logs about fake APs if peri | Default: 1 | Min: 1 | Max: 1440
    sta_offline_cleanup: int  # Time period in seconds to keep station offline dat | Default: 300 | Min: 0 | Max: 4294967295
    sta_offline_ip2mac_cleanup: int  # Time period in seconds to keep station offline Ip2 | Default: 300 | Min: 0 | Max: 4294967295
    sta_cap_cleanup: int  # Time period in minutes to keep station capability | Default: 0 | Min: 0 | Max: 4294967295
    rogue_ap_cleanup: int  # Time period in minutes to keep rogue AP after it i | Default: 0 | Min: 0 | Max: 4294967295
    rogue_sta_cleanup: int  # Time period in minutes to keep rogue station after | Default: 0 | Min: 0 | Max: 4294967295
    wids_entry_cleanup: int  # Time period in minutes to keep wids entry after it | Default: 0 | Min: 0 | Max: 4294967295
    ble_device_cleanup: int  # Time period in minutes to keep BLE device after it | Default: 60 | Min: 0 | Max: 4294967295
    sta_stats_interval: int  # Time between running client (station) reports | Default: 10 | Min: 1 | Max: 255
    vap_stats_interval: int  # Time between running Virtual Access Point (VAP) re | Default: 15 | Min: 1 | Max: 255
    radio_stats_interval: int  # Time between running radio reports | Default: 15 | Min: 1 | Max: 255
    sta_capability_interval: int  # Time between running station capability reports | Default: 30 | Min: 1 | Max: 255
    sta_locate_timer: int  # Time between running client presence flushes to re | Default: 1800 | Min: 0 | Max: 86400
    ipsec_intf_cleanup: int  # Time period to keep IPsec VPN interfaces up after | Default: 120 | Min: 30 | Max: 3600
    ble_scan_report_intv: int  # Time between running Bluetooth Low Energy (BLE) re | Default: 30 | Min: 10 | Max: 3600
    drma_interval: int  # Dynamic radio mode assignment (DRMA) schedule inte | Default: 60 | Min: 1 | Max: 1440
    ap_reboot_wait_interval1: int  # Time in minutes to wait before AP reboots when the | Default: 0 | Min: 5 | Max: 65535
    ap_reboot_wait_time: str  # Time to reboot the AP when there is no controller | MaxLen: 7
    ap_reboot_wait_interval2: int  # Time in minutes to wait before AP reboots when the | Default: 0 | Min: 5 | Max: 65535


@final
class TimersObject:
    """Typed FortiObject for wireless_controller/timers with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Time between echo requests sent by the managed WTP, AP, or F | Default: 30 | Min: 1 | Max: 255
    echo_interval: int
    # Maximal time in seconds between control requests sent by the | Default: 0 | Min: 0 | Max: 255
    nat_session_keep_alive: int
    # Time between discovery requests (2 - 180 sec, default = 5). | Default: 5 | Min: 2 | Max: 180
    discovery_interval: int
    # Time after which a client is considered idle and times out | Default: 300 | Min: 20 | Max: 3600
    client_idle_timeout: int
    # Time after which a client is considered idle and disconnecte | Default: 20 | Min: 2 | Max: 3600
    client_idle_rehome_timeout: int
    # Time after which a client is considered failed in RADIUS aut | Default: 5 | Min: 5 | Max: 30
    auth_timeout: int
    # Time between logging rogue AP messages if periodic rogue AP | Default: 0 | Min: 0 | Max: 1440
    rogue_ap_log: int
    # Time between recording logs about fake APs if periodic fake | Default: 1 | Min: 1 | Max: 1440
    fake_ap_log: int
    # Time period in seconds to keep station offline data after it | Default: 300 | Min: 0 | Max: 4294967295
    sta_offline_cleanup: int
    # Time period in seconds to keep station offline Ip2mac data a | Default: 300 | Min: 0 | Max: 4294967295
    sta_offline_ip2mac_cleanup: int
    # Time period in minutes to keep station capability data after | Default: 0 | Min: 0 | Max: 4294967295
    sta_cap_cleanup: int
    # Time period in minutes to keep rogue AP after it is gone | Default: 0 | Min: 0 | Max: 4294967295
    rogue_ap_cleanup: int
    # Time period in minutes to keep rogue station after it is gon | Default: 0 | Min: 0 | Max: 4294967295
    rogue_sta_cleanup: int
    # Time period in minutes to keep wids entry after it is gone | Default: 0 | Min: 0 | Max: 4294967295
    wids_entry_cleanup: int
    # Time period in minutes to keep BLE device after it is gone | Default: 60 | Min: 0 | Max: 4294967295
    ble_device_cleanup: int
    # Time between running client (station) reports | Default: 10 | Min: 1 | Max: 255
    sta_stats_interval: int
    # Time between running Virtual Access Point (VAP) reports | Default: 15 | Min: 1 | Max: 255
    vap_stats_interval: int
    # Time between running radio reports | Default: 15 | Min: 1 | Max: 255
    radio_stats_interval: int
    # Time between running station capability reports | Default: 30 | Min: 1 | Max: 255
    sta_capability_interval: int
    # Time between running client presence flushes to remove clien | Default: 1800 | Min: 0 | Max: 86400
    sta_locate_timer: int
    # Time period to keep IPsec VPN interfaces up after WTP sessio | Default: 120 | Min: 30 | Max: 3600
    ipsec_intf_cleanup: int
    # Time between running Bluetooth Low Energy (BLE) reports | Default: 30 | Min: 10 | Max: 3600
    ble_scan_report_intv: int
    # Dynamic radio mode assignment (DRMA) schedule interval in mi | Default: 60 | Min: 1 | Max: 1440
    drma_interval: int
    # Time in minutes to wait before AP reboots when there is no c | Default: 0 | Min: 5 | Max: 65535
    ap_reboot_wait_interval1: int
    # Time to reboot the AP when there is no controller detected a | MaxLen: 7
    ap_reboot_wait_time: str
    # Time in minutes to wait before AP reboots when there is no c | Default: 0 | Min: 5 | Max: 65535
    ap_reboot_wait_interval2: int
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> TimersPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Timers:
    """
    Configure CAPWAP timers.
    
    Path: wireless_controller/timers
    Category: cmdb
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
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> TimersResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> TimersResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        name: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> TimersResponse: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        name: str,
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
    ) -> TimersObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        name: str,
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
    ) -> TimersObject: ...
    
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
    ) -> TimersObject: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        name: str | None = ...,
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
        name: str,
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
    ) -> TimersResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        name: str,
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
    ) -> TimersResponse: ...
    
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
    ) -> TimersResponse: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        name: str | None = ...,
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
    ) -> dict[str, Any] | FortiObject: ...
    
    def get(
        self,
        name: str | None = ...,
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
    ) -> TimersObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TimersObject: ...
    
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
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

class TimersDictMode:
    """Timers endpoint for dict response mode (default for this client).
    
    By default returns TimersResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return TimersObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        name: str | None = ...,
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
        name: str,
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
    ) -> TimersObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        name: None = ...,
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
    ) -> TimersObject: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        name: str,
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
    ) -> TimersResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        name: None = ...,
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
    ) -> TimersResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TimersObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...


    # Helper methods (inherited from base class)
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
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


class TimersObjectMode:
    """Timers endpoint for object response mode (default for this client).
    
    By default returns TimersObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return TimersResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        name: str | None = ...,
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
        name: str,
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
    ) -> TimersResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        name: None = ...,
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
    ) -> TimersResponse: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        name: str,
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
    ) -> TimersObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        name: None = ...,
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
    ) -> TimersObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TimersObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> TimersObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...


    # Helper methods (inherited from base class)
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: TimersPayload | None = ...,
        echo_interval: int | None = ...,
        nat_session_keep_alive: int | None = ...,
        discovery_interval: int | None = ...,
        client_idle_timeout: int | None = ...,
        client_idle_rehome_timeout: int | None = ...,
        auth_timeout: int | None = ...,
        rogue_ap_log: int | None = ...,
        fake_ap_log: int | None = ...,
        sta_offline_cleanup: int | None = ...,
        sta_offline_ip2mac_cleanup: int | None = ...,
        sta_cap_cleanup: int | None = ...,
        rogue_ap_cleanup: int | None = ...,
        rogue_sta_cleanup: int | None = ...,
        wids_entry_cleanup: int | None = ...,
        ble_device_cleanup: int | None = ...,
        sta_stats_interval: int | None = ...,
        vap_stats_interval: int | None = ...,
        radio_stats_interval: int | None = ...,
        sta_capability_interval: int | None = ...,
        sta_locate_timer: int | None = ...,
        ipsec_intf_cleanup: int | None = ...,
        ble_scan_report_intv: int | None = ...,
        drma_interval: int | None = ...,
        ap_reboot_wait_interval1: int | None = ...,
        ap_reboot_wait_time: str | None = ...,
        ap_reboot_wait_interval2: int | None = ...,
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
    "Timers",
    "TimersDictMode",
    "TimersObjectMode",
    "TimersPayload",
    "TimersObject",
]