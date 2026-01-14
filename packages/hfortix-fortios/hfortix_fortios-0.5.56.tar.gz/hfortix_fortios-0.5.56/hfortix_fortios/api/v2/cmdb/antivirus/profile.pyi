from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ProfilePayload(TypedDict, total=False):
    """
    Type hints for antivirus/profile payload fields.
    
    Configure AntiVirus profiles.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.dlp.filepattern.FilepatternEndpoint` (via: analytics-accept-filetype, analytics-ignore-filetype)
        - :class:`~.system.replacemsg-group.ReplacemsgGroupEndpoint` (via: replacemsg-group)

    **Usage:**
        payload: ProfilePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Profile name. | MaxLen: 47
    comment: str  # Comment. | MaxLen: 255
    replacemsg_group: str  # Replacement message group customized for this prof | MaxLen: 35
    feature_set: Literal["flow", "proxy"]  # Flow/proxy feature set. | Default: flow
    fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"]  # FortiSandbox scan modes. | Default: analytics-everything
    fortisandbox_max_upload: int  # Maximum size of files that can be uploaded to Fort | Default: 10 | Min: 1 | Max: 4095
    analytics_ignore_filetype: int  # Do not submit files matching this DLP file-pattern | Default: 0 | Min: 0 | Max: 4294967295
    analytics_accept_filetype: int  # Only submit files matching this DLP file-pattern t | Default: 0 | Min: 0 | Max: 4294967295
    analytics_db: Literal["disable", "enable"]  # Enable/disable using the FortiSandbox signature da | Default: disable
    mobile_malware_db: Literal["disable", "enable"]  # Enable/disable using the mobile malware signature | Default: enable
    http: str  # Configure HTTP AntiVirus options.
    ftp: str  # Configure FTP AntiVirus options.
    imap: str  # Configure IMAP AntiVirus options.
    pop3: str  # Configure POP3 AntiVirus options.
    smtp: str  # Configure SMTP AntiVirus options.
    mapi: str  # Configure MAPI AntiVirus options.
    nntp: str  # Configure NNTP AntiVirus options.
    cifs: str  # Configure CIFS AntiVirus options.
    ssh: str  # Configure SFTP and SCP AntiVirus options.
    nac_quar: str  # Configure AntiVirus quarantine settings.
    content_disarm: str  # AV Content Disarm and Reconstruction settings.
    outbreak_prevention_archive_scan: Literal["disable", "enable"]  # Enable/disable outbreak-prevention archive scannin | Default: enable
    external_blocklist_enable_all: Literal["disable", "enable"]  # Enable/disable all external blocklists. | Default: disable
    external_blocklist: list[dict[str, Any]]  # One or more external malware block lists.
    ems_threat_feed: Literal["disable", "enable"]  # Enable/disable use of EMS threat feed when perform | Default: disable
    fortindr_error_action: Literal["log-only", "block", "ignore"]  # Action to take if FortiNDR encounters an error. | Default: log-only
    fortindr_timeout_action: Literal["log-only", "block", "ignore"]  # Action to take if FortiNDR encounters a scan timeo | Default: log-only
    fortisandbox_scan_timeout: int  # FortiSandbox inline scan timeout in seconds | Default: 60 | Min: 30 | Max: 180
    fortisandbox_error_action: Literal["log-only", "block", "ignore"]  # Action to take if FortiSandbox inline scan encount | Default: log-only
    fortisandbox_timeout_action: Literal["log-only", "block", "ignore"]  # Action to take if FortiSandbox inline scan encount | Default: log-only
    av_virus_log: Literal["enable", "disable"]  # Enable/disable AntiVirus logging. | Default: enable
    extended_log: Literal["enable", "disable"]  # Enable/disable extended logging for antivirus. | Default: disable
    scan_mode: Literal["default", "legacy"]  # Configure scan mode (default or legacy). | Default: default

# Nested TypedDicts for table field children (dict mode)

class ProfileExternalblocklistItem(TypedDict):
    """Type hints for external-blocklist table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # External blocklist. | MaxLen: 79


# Nested classes for table field children (object mode)

@final
class ProfileExternalblocklistObject:
    """Typed object for external-blocklist table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # External blocklist. | MaxLen: 79
    name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class ProfileResponse(TypedDict):
    """
    Type hints for antivirus/profile API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Profile name. | MaxLen: 47
    comment: str  # Comment. | MaxLen: 255
    replacemsg_group: str  # Replacement message group customized for this prof | MaxLen: 35
    feature_set: Literal["flow", "proxy"]  # Flow/proxy feature set. | Default: flow
    fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"]  # FortiSandbox scan modes. | Default: analytics-everything
    fortisandbox_max_upload: int  # Maximum size of files that can be uploaded to Fort | Default: 10 | Min: 1 | Max: 4095
    analytics_ignore_filetype: int  # Do not submit files matching this DLP file-pattern | Default: 0 | Min: 0 | Max: 4294967295
    analytics_accept_filetype: int  # Only submit files matching this DLP file-pattern t | Default: 0 | Min: 0 | Max: 4294967295
    analytics_db: Literal["disable", "enable"]  # Enable/disable using the FortiSandbox signature da | Default: disable
    mobile_malware_db: Literal["disable", "enable"]  # Enable/disable using the mobile malware signature | Default: enable
    http: str  # Configure HTTP AntiVirus options.
    ftp: str  # Configure FTP AntiVirus options.
    imap: str  # Configure IMAP AntiVirus options.
    pop3: str  # Configure POP3 AntiVirus options.
    smtp: str  # Configure SMTP AntiVirus options.
    mapi: str  # Configure MAPI AntiVirus options.
    nntp: str  # Configure NNTP AntiVirus options.
    cifs: str  # Configure CIFS AntiVirus options.
    ssh: str  # Configure SFTP and SCP AntiVirus options.
    nac_quar: str  # Configure AntiVirus quarantine settings.
    content_disarm: str  # AV Content Disarm and Reconstruction settings.
    outbreak_prevention_archive_scan: Literal["disable", "enable"]  # Enable/disable outbreak-prevention archive scannin | Default: enable
    external_blocklist_enable_all: Literal["disable", "enable"]  # Enable/disable all external blocklists. | Default: disable
    external_blocklist: list[ProfileExternalblocklistItem]  # One or more external malware block lists.
    ems_threat_feed: Literal["disable", "enable"]  # Enable/disable use of EMS threat feed when perform | Default: disable
    fortindr_error_action: Literal["log-only", "block", "ignore"]  # Action to take if FortiNDR encounters an error. | Default: log-only
    fortindr_timeout_action: Literal["log-only", "block", "ignore"]  # Action to take if FortiNDR encounters a scan timeo | Default: log-only
    fortisandbox_scan_timeout: int  # FortiSandbox inline scan timeout in seconds | Default: 60 | Min: 30 | Max: 180
    fortisandbox_error_action: Literal["log-only", "block", "ignore"]  # Action to take if FortiSandbox inline scan encount | Default: log-only
    fortisandbox_timeout_action: Literal["log-only", "block", "ignore"]  # Action to take if FortiSandbox inline scan encount | Default: log-only
    av_virus_log: Literal["enable", "disable"]  # Enable/disable AntiVirus logging. | Default: enable
    extended_log: Literal["enable", "disable"]  # Enable/disable extended logging for antivirus. | Default: disable
    scan_mode: Literal["default", "legacy"]  # Configure scan mode (default or legacy). | Default: default


@final
class ProfileObject:
    """Typed FortiObject for antivirus/profile with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Profile name. | MaxLen: 47
    name: str
    # Comment. | MaxLen: 255
    comment: str
    # Replacement message group customized for this profile. | MaxLen: 35
    replacemsg_group: str
    # Flow/proxy feature set. | Default: flow
    feature_set: Literal["flow", "proxy"]
    # FortiSandbox scan modes. | Default: analytics-everything
    fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"]
    # Maximum size of files that can be uploaded to FortiSandbox i | Default: 10 | Min: 1 | Max: 4095
    fortisandbox_max_upload: int
    # Do not submit files matching this DLP file-pattern to FortiS | Default: 0 | Min: 0 | Max: 4294967295
    analytics_ignore_filetype: int
    # Only submit files matching this DLP file-pattern to FortiSan | Default: 0 | Min: 0 | Max: 4294967295
    analytics_accept_filetype: int
    # Enable/disable using the FortiSandbox signature database to | Default: disable
    analytics_db: Literal["disable", "enable"]
    # Enable/disable using the mobile malware signature database. | Default: enable
    mobile_malware_db: Literal["disable", "enable"]
    # Configure HTTP AntiVirus options.
    http: str
    # Configure FTP AntiVirus options.
    ftp: str
    # Configure IMAP AntiVirus options.
    imap: str
    # Configure POP3 AntiVirus options.
    pop3: str
    # Configure SMTP AntiVirus options.
    smtp: str
    # Configure MAPI AntiVirus options.
    mapi: str
    # Configure NNTP AntiVirus options.
    nntp: str
    # Configure CIFS AntiVirus options.
    cifs: str
    # Configure SFTP and SCP AntiVirus options.
    ssh: str
    # Configure AntiVirus quarantine settings.
    nac_quar: str
    # AV Content Disarm and Reconstruction settings.
    content_disarm: str
    # Enable/disable outbreak-prevention archive scanning. | Default: enable
    outbreak_prevention_archive_scan: Literal["disable", "enable"]
    # Enable/disable all external blocklists. | Default: disable
    external_blocklist_enable_all: Literal["disable", "enable"]
    # One or more external malware block lists.
    external_blocklist: list[ProfileExternalblocklistObject]
    # Enable/disable use of EMS threat feed when performing AntiVi | Default: disable
    ems_threat_feed: Literal["disable", "enable"]
    # Action to take if FortiNDR encounters an error. | Default: log-only
    fortindr_error_action: Literal["log-only", "block", "ignore"]
    # Action to take if FortiNDR encounters a scan timeout. | Default: log-only
    fortindr_timeout_action: Literal["log-only", "block", "ignore"]
    # FortiSandbox inline scan timeout in seconds | Default: 60 | Min: 30 | Max: 180
    fortisandbox_scan_timeout: int
    # Action to take if FortiSandbox inline scan encounters an err | Default: log-only
    fortisandbox_error_action: Literal["log-only", "block", "ignore"]
    # Action to take if FortiSandbox inline scan encounters a scan | Default: log-only
    fortisandbox_timeout_action: Literal["log-only", "block", "ignore"]
    # Enable/disable AntiVirus logging. | Default: enable
    av_virus_log: Literal["enable", "disable"]
    # Enable/disable extended logging for antivirus. | Default: disable
    extended_log: Literal["enable", "disable"]
    # Configure scan mode (default or legacy). | Default: default
    scan_mode: Literal["default", "legacy"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ProfilePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Profile:
    """
    Configure AntiVirus profiles.
    
    Path: antivirus/profile
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
    ) -> ProfileResponse: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject | list[ProfileObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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

class ProfileDictMode:
    """Profile endpoint for dict response mode (default for this client).
    
    By default returns ProfileResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ProfileObject.
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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


class ProfileObjectMode:
    """Profile endpoint for object response mode (default for this client).
    
    By default returns ProfileObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ProfileResponse (TypedDict).
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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
    ) -> ProfileObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: str | None = ...,
        ftp: str | None = ...,
        imap: str | None = ...,
        pop3: str | None = ...,
        smtp: str | None = ...,
        mapi: str | None = ...,
        nntp: str | None = ...,
        cifs: str | None = ...,
        ssh: str | None = ...,
        nac_quar: str | None = ...,
        content_disarm: str | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[dict[str, Any]] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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
    "Profile",
    "ProfileDictMode",
    "ProfileObjectMode",
    "ProfilePayload",
    "ProfileObject",
]