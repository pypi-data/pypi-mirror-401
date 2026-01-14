from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class H2qpConnCapabilityPayload(TypedDict, total=False):
    """
    Type hints for wireless_controller/hotspot20/h2qp_conn_capability payload fields.
    
    Configure connection capability.
    
    **Usage:**
        payload: H2qpConnCapabilityPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Connection capability name. | MaxLen: 35
    icmp_port: Literal["closed", "open", "unknown"]  # Set ICMP port service status. | Default: unknown
    ftp_port: Literal["closed", "open", "unknown"]  # Set FTP port service status. | Default: unknown
    ssh_port: Literal["closed", "open", "unknown"]  # Set SSH port service status. | Default: unknown
    http_port: Literal["closed", "open", "unknown"]  # Set HTTP port service status. | Default: unknown
    tls_port: Literal["closed", "open", "unknown"]  # Set TLS VPN (HTTPS) port service status. | Default: unknown
    pptp_vpn_port: Literal["closed", "open", "unknown"]  # Set Point to Point Tunneling Protocol (PPTP) VPN p | Default: unknown
    voip_tcp_port: Literal["closed", "open", "unknown"]  # Set VoIP TCP port service status. | Default: unknown
    voip_udp_port: Literal["closed", "open", "unknown"]  # Set VoIP UDP port service status. | Default: unknown
    ikev2_port: Literal["closed", "open", "unknown"]  # Set IKEv2 port service for IPsec VPN status. | Default: unknown
    ikev2_xx_port: Literal["closed", "open", "unknown"]  # Set UDP port 4500 | Default: unknown
    esp_port: Literal["closed", "open", "unknown"]  # Set ESP port service (used by IPsec VPNs) status. | Default: unknown

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class H2qpConnCapabilityResponse(TypedDict):
    """
    Type hints for wireless_controller/hotspot20/h2qp_conn_capability API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Connection capability name. | MaxLen: 35
    icmp_port: Literal["closed", "open", "unknown"]  # Set ICMP port service status. | Default: unknown
    ftp_port: Literal["closed", "open", "unknown"]  # Set FTP port service status. | Default: unknown
    ssh_port: Literal["closed", "open", "unknown"]  # Set SSH port service status. | Default: unknown
    http_port: Literal["closed", "open", "unknown"]  # Set HTTP port service status. | Default: unknown
    tls_port: Literal["closed", "open", "unknown"]  # Set TLS VPN (HTTPS) port service status. | Default: unknown
    pptp_vpn_port: Literal["closed", "open", "unknown"]  # Set Point to Point Tunneling Protocol (PPTP) VPN p | Default: unknown
    voip_tcp_port: Literal["closed", "open", "unknown"]  # Set VoIP TCP port service status. | Default: unknown
    voip_udp_port: Literal["closed", "open", "unknown"]  # Set VoIP UDP port service status. | Default: unknown
    ikev2_port: Literal["closed", "open", "unknown"]  # Set IKEv2 port service for IPsec VPN status. | Default: unknown
    ikev2_xx_port: Literal["closed", "open", "unknown"]  # Set UDP port 4500 | Default: unknown
    esp_port: Literal["closed", "open", "unknown"]  # Set ESP port service (used by IPsec VPNs) status. | Default: unknown


@final
class H2qpConnCapabilityObject:
    """Typed FortiObject for wireless_controller/hotspot20/h2qp_conn_capability with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Connection capability name. | MaxLen: 35
    name: str
    # Set ICMP port service status. | Default: unknown
    icmp_port: Literal["closed", "open", "unknown"]
    # Set FTP port service status. | Default: unknown
    ftp_port: Literal["closed", "open", "unknown"]
    # Set SSH port service status. | Default: unknown
    ssh_port: Literal["closed", "open", "unknown"]
    # Set HTTP port service status. | Default: unknown
    http_port: Literal["closed", "open", "unknown"]
    # Set TLS VPN (HTTPS) port service status. | Default: unknown
    tls_port: Literal["closed", "open", "unknown"]
    # Set Point to Point Tunneling Protocol (PPTP) VPN port servic | Default: unknown
    pptp_vpn_port: Literal["closed", "open", "unknown"]
    # Set VoIP TCP port service status. | Default: unknown
    voip_tcp_port: Literal["closed", "open", "unknown"]
    # Set VoIP UDP port service status. | Default: unknown
    voip_udp_port: Literal["closed", "open", "unknown"]
    # Set IKEv2 port service for IPsec VPN status. | Default: unknown
    ikev2_port: Literal["closed", "open", "unknown"]
    # Set UDP port 4500 (which may be used by IKEv2 for IPsec VPN) | Default: unknown
    ikev2_xx_port: Literal["closed", "open", "unknown"]
    # Set ESP port service (used by IPsec VPNs) status. | Default: unknown
    esp_port: Literal["closed", "open", "unknown"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> H2qpConnCapabilityPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class H2qpConnCapability:
    """
    Configure connection capability.
    
    Path: wireless_controller/hotspot20/h2qp_conn_capability
    Category: cmdb
    Primary Key: name
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
    ) -> H2qpConnCapabilityResponse: ...
    
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
    ) -> H2qpConnCapabilityResponse: ...
    
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
    ) -> list[H2qpConnCapabilityResponse]: ...
    
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
    ) -> H2qpConnCapabilityObject: ...
    
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
    ) -> H2qpConnCapabilityObject: ...
    
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
    ) -> list[H2qpConnCapabilityObject]: ...
    
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
    ) -> H2qpConnCapabilityResponse: ...
    
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
    ) -> H2qpConnCapabilityResponse: ...
    
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
    ) -> list[H2qpConnCapabilityResponse]: ...
    
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
    ) -> Union[dict[str, Any], list[dict[str, Any]], FortiObject, list[FortiObject]]: ...
    
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
    ) -> H2qpConnCapabilityObject | list[H2qpConnCapabilityObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    @overload
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
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

class H2qpConnCapabilityDictMode:
    """H2qpConnCapability endpoint for dict response mode (default for this client).
    
    By default returns H2qpConnCapabilityResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return H2qpConnCapabilityObject.
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
    ) -> H2qpConnCapabilityObject: ...
    
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
    ) -> list[H2qpConnCapabilityObject]: ...
    
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
    ) -> H2qpConnCapabilityResponse: ...
    
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
    ) -> list[H2qpConnCapabilityResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        name: str,
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
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
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


class H2qpConnCapabilityObjectMode:
    """H2qpConnCapability endpoint for object response mode (default for this client).
    
    By default returns H2qpConnCapabilityObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return H2qpConnCapabilityResponse (TypedDict).
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
    ) -> H2qpConnCapabilityResponse: ...
    
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
    ) -> list[H2qpConnCapabilityResponse]: ...
    
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
    ) -> H2qpConnCapabilityObject: ...
    
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
    ) -> list[H2qpConnCapabilityObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> H2qpConnCapabilityObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        name: str,
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
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
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
    "H2qpConnCapability",
    "H2qpConnCapabilityDictMode",
    "H2qpConnCapabilityObjectMode",
    "H2qpConnCapabilityPayload",
    "H2qpConnCapabilityObject",
]