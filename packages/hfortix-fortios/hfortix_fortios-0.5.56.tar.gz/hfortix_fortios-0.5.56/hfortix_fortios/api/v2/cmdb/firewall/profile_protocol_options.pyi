from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ProfileProtocolOptionsPayload(TypedDict, total=False):
    """
    Type hints for firewall/profile_protocol_options payload fields.
    
    Configure protocol options.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.replacemsg-group.ReplacemsgGroupEndpoint` (via: replacemsg-group)

    **Usage:**
        payload: ProfileProtocolOptionsPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name. | MaxLen: 47
    comment: str  # Optional comments. | MaxLen: 255
    replacemsg_group: str  # Name of the replacement message group to be used. | MaxLen: 35
    oversize_log: Literal["disable", "enable"]  # Enable/disable logging for antivirus oversize file | Default: disable
    switching_protocols_log: Literal["disable", "enable"]  # Enable/disable logging for HTTP/HTTPS switching pr | Default: disable
    http: str  # Configure HTTP protocol options.
    ftp: str  # Configure FTP protocol options.
    imap: str  # Configure IMAP protocol options.
    mapi: str  # Configure MAPI protocol options.
    pop3: str  # Configure POP3 protocol options.
    smtp: str  # Configure SMTP protocol options.
    nntp: str  # Configure NNTP protocol options.
    ssh: str  # Configure SFTP and SCP protocol options.
    dns: str  # Configure DNS protocol options.
    cifs: str  # Configure CIFS protocol options.
    mail_signature: str  # Configure Mail signature.
    rpc_over_http: Literal["enable", "disable"]  # Enable/disable inspection of RPC over HTTP. | Default: disable

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class ProfileProtocolOptionsResponse(TypedDict):
    """
    Type hints for firewall/profile_protocol_options API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name. | MaxLen: 47
    comment: str  # Optional comments. | MaxLen: 255
    replacemsg_group: str  # Name of the replacement message group to be used. | MaxLen: 35
    oversize_log: Literal["disable", "enable"]  # Enable/disable logging for antivirus oversize file | Default: disable
    switching_protocols_log: Literal["disable", "enable"]  # Enable/disable logging for HTTP/HTTPS switching pr | Default: disable
    http: str  # Configure HTTP protocol options.
    ftp: str  # Configure FTP protocol options.
    imap: str  # Configure IMAP protocol options.
    mapi: str  # Configure MAPI protocol options.
    pop3: str  # Configure POP3 protocol options.
    smtp: str  # Configure SMTP protocol options.
    nntp: str  # Configure NNTP protocol options.
    ssh: str  # Configure SFTP and SCP protocol options.
    dns: str  # Configure DNS protocol options.
    cifs: str  # Configure CIFS protocol options.
    mail_signature: str  # Configure Mail signature.
    rpc_over_http: Literal["enable", "disable"]  # Enable/disable inspection of RPC over HTTP. | Default: disable


@final
class ProfileProtocolOptionsObject:
    """Typed FortiObject for firewall/profile_protocol_options with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name. | MaxLen: 47
    name: str
    # Optional comments. | MaxLen: 255
    comment: str
    # Name of the replacement message group to be used. | MaxLen: 35
    replacemsg_group: str
    # Enable/disable logging for antivirus oversize file blocking. | Default: disable
    oversize_log: Literal["disable", "enable"]
    # Enable/disable logging for HTTP/HTTPS switching protocols. | Default: disable
    switching_protocols_log: Literal["disable", "enable"]
    # Configure HTTP protocol options.
    http: str
    # Configure FTP protocol options.
    ftp: str
    # Configure IMAP protocol options.
    imap: str
    # Configure MAPI protocol options.
    mapi: str
    # Configure POP3 protocol options.
    pop3: str
    # Configure SMTP protocol options.
    smtp: str
    # Configure NNTP protocol options.
    nntp: str
    # Configure SFTP and SCP protocol options.
    ssh: str
    # Configure DNS protocol options.
    dns: str
    # Configure CIFS protocol options.
    cifs: str
    # Configure Mail signature.
    mail_signature: str
    # Enable/disable inspection of RPC over HTTP. | Default: disable
    rpc_over_http: Literal["enable", "disable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ProfileProtocolOptionsPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class ProfileProtocolOptions:
    """
    Configure protocol options.
    
    Path: firewall/profile_protocol_options
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
    ) -> ProfileProtocolOptionsResponse: ...
    
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
    ) -> ProfileProtocolOptionsResponse: ...
    
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
    ) -> list[ProfileProtocolOptionsResponse]: ...
    
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
    ) -> ProfileProtocolOptionsObject: ...
    
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
    ) -> ProfileProtocolOptionsObject: ...
    
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
    ) -> list[ProfileProtocolOptionsObject]: ...
    
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
    ) -> ProfileProtocolOptionsResponse: ...
    
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
    ) -> ProfileProtocolOptionsResponse: ...
    
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
    ) -> list[ProfileProtocolOptionsResponse]: ...
    
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
    ) -> ProfileProtocolOptionsObject | list[ProfileProtocolOptionsObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
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
    ) -> ProfileProtocolOptionsObject: ...
    
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
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
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

class ProfileProtocolOptionsDictMode:
    """ProfileProtocolOptions endpoint for dict response mode (default for this client).
    
    By default returns ProfileProtocolOptionsResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ProfileProtocolOptionsObject.
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
    ) -> ProfileProtocolOptionsObject: ...
    
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
    ) -> list[ProfileProtocolOptionsObject]: ...
    
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
    ) -> ProfileProtocolOptionsResponse: ...
    
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
    ) -> list[ProfileProtocolOptionsResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
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
    ) -> ProfileProtocolOptionsObject: ...
    
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
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
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


class ProfileProtocolOptionsObjectMode:
    """ProfileProtocolOptions endpoint for object response mode (default for this client).
    
    By default returns ProfileProtocolOptionsObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ProfileProtocolOptionsResponse (TypedDict).
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
    ) -> ProfileProtocolOptionsResponse: ...
    
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
    ) -> list[ProfileProtocolOptionsResponse]: ...
    
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
    ) -> ProfileProtocolOptionsObject: ...
    
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
    ) -> list[ProfileProtocolOptionsObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
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
    ) -> ProfileProtocolOptionsObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileProtocolOptionsObject: ...
    
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
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        mapi: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        nntp: str | None = ...,
        ssh: str | None = ...,
        dns: str | None = ...,
        cifs: str | None = ...,
        mail_signature: str | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
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
    "ProfileProtocolOptions",
    "ProfileProtocolOptionsDictMode",
    "ProfileProtocolOptionsObjectMode",
    "ProfileProtocolOptionsPayload",
    "ProfileProtocolOptionsObject",
]