"""
Payload building helpers for FortiOS API.

Converts Python-style parameters to FortiOS API payloads with:
- snake_case to kebab-case conversion
- Optional list normalization
- None value filtering
"""

from typing import Any

from hfortix_fortios._helpers.normalizers import normalize_to_name_list


def build_cmdb_payload(**params: Any) -> dict[str, Any]:
    """
    Build a CMDB payload dictionary from keyword arguments (API layer - no normalization).

    Converts Python snake_case parameter names to FortiOS kebab-case API keys
    and filters out None values. This is the base helper used by all CMDB API endpoints.

    Does NOT normalize list fields - caller is responsible for providing data
    in the correct FortiOS format (unless using a wrapper with normalization).

    Args:
        **params: All resource parameters (e.g., name=..., member=..., etc.)

    Returns:
        Dictionary with FortiOS API-compatible keys and non-None values
    """
    payload: dict[str, Any] = {}

    # Extract 'data' parameter if present
    # It should be merged, not added as a key
    data_dict = params.pop("data", None)

    for param_name, value in params.items():
        if value is None:
            continue

        # Convert snake_case to kebab-case for FortiOS API
        api_key = param_name.replace("_", "-")
        payload[api_key] = value

    # Merge 'data' dictionary into payload (override existing keys)
    if data_dict and isinstance(data_dict, dict):
        payload.update(data_dict)

    return payload


def build_cmdb_payload_normalized(
    normalize_fields: set[str] | None = None, **params: Any
) -> dict[str, Any]:
    """
    Build a CMDB payload with automatic normalization (convenience wrapper layer).

    Converts Python snake_case parameter names to FortiOS kebab-case API keys,
    filters out None values, AND normalizes specified list fields to FortiOS format.

    This is used by convenience wrappers to accept flexible inputs like strings
    or lists and automatically convert them to FortiOS [{'name': '...'}] format.

    Args:
        normalize_fields: Set of field names (snake_case) that should be normalized
                         to [{'name': '...'}] format. If None, common fields like
                         'member', 'interface', 'allowaccess' are normalized.
        **params: All resource parameters

    Returns:
        Dictionary with FortiOS API-compatible keys and normalized values
    """
    # Default fields that commonly need normalization across CMDB endpoints
    DEFAULT_NORMALIZE_FIELDS = {
        "member",  # address groups, service groups, user groups
        "interface",  # various config objects
        "allowaccess",  # system interfaces
        "srcintf",  # firewall policies, routes
        "dstintf",  # firewall policies, routes
        "srcaddr",  # firewall policies
        "dstaddr",  # firewall policies
        "service",  # firewall policies
        "users",  # various auth/policy objects
        "groups",  # various auth/policy objects
    }

    # Use provided fields or defaults
    fields_to_normalize = (
        normalize_fields
        if normalize_fields is not None
        else DEFAULT_NORMALIZE_FIELDS
    )

    payload: dict[str, Any] = {}

    # Extract 'data' parameter if present
    # It should be merged, not added as a key
    data_dict = params.pop("data", None)

    for param_name, value in params.items():
        if value is None:
            continue

        # Convert snake_case to kebab-case for FortiOS API
        api_key = param_name.replace("_", "-")

        # Normalize list parameters to FortiOS format if specified
        if param_name in fields_to_normalize:
            normalized = normalize_to_name_list(value)
            # Only add if normalization resulted in non-empty list
            if normalized:
                payload[api_key] = normalized
        else:
            payload[api_key] = value

    # Merge 'data' dictionary into payload (override existing keys)
    if data_dict and isinstance(data_dict, dict):
        payload.update(data_dict)

    return payload


def build_api_payload(
    normalize_fields: set[str] | None = None,
    auto_normalize: bool = True,
    **params: Any,
) -> dict[str, Any]:
    """
    Build a generic API payload with intelligent list normalization.

    Universal helper for all API types (cmdb, monitor, log, service).
    Automatically normalizes common list fields that use [{'name': '...'}] format.

    Args:
        normalize_fields: Explicit set of field names (snake_case) to normalize.
                         If provided, only these fields are normalized.
        auto_normalize: If True and normalize_fields is None, auto-detect and
                       normalize common list fields. Set False for raw passthrough.
        **params: All resource parameters

    Returns:
        Dictionary with FortiOS API-compatible keys and normalized values
    """
    # Common list fields across all API types that use [{'name': '...'}] format
    COMMON_LIST_FIELDS = {
        # Firewall policy fields
        "srcintf",
        "dstintf",
        "srcaddr",
        "dstaddr",
        "srcaddr6",
        "dstaddr6",
        "service",
        "poolname",
        "poolname6",
        "groups",
        "users",
        "fsso_groups",
        "ztna_ems_tag",
        "ztna_ems_tag_secondary",
        "ztna_geo_tag",
        "internet_service_name",
        "internet_service_group",
        "internet_service_custom",
        "internet_service_custom_group",
        "network_service_dynamic",
        "internet_service_src_name",
        "internet_service_src_group",
        "internet_service_src_custom",
        "internet_service_src_custom_group",
        "network_service_src_dynamic",
        "internet_service6_name",
        "internet_service6_group",
        "internet_service6_custom",
        "internet_service6_custom_group",
        "internet_service6_src_name",
        "internet_service6_src_group",
        "internet_service6_src_custom",
        "internet_service6_src_custom_group",
        "src_vendor_mac",
        "rtp_addr",
        "ntlm_enabled_browsers",
        "custom_log_fields",
        "pcp_poolname",
        "sgt",
        "internet_service_fortiguard",
        "internet_service_src_fortiguard",
        "internet_service6_fortiguard",
        "internet_service6_src_fortiguard",
        # Group membership
        "member",
        # System/interface fields
        "interface",
        "allowaccess",
        "device",
        # Router fields
        "gateway",
        "nexthop",
        # VPN fields
        "destination",
        "source",
        # Application fields
        "application",
        "category",
        # User fields
        "group",
        "user",
        # Certificate fields
        "ca",
        "certificate",
        # DNS fields
        "dns_server",
    }

    # Determine which fields to normalize
    if normalize_fields is not None:
        # Explicit field list provided
        fields_to_normalize = normalize_fields
    elif auto_normalize:
        # Auto-detect common fields
        fields_to_normalize = COMMON_LIST_FIELDS
    else:
        # No normalization
        fields_to_normalize = set()

    payload: dict[str, Any] = {}

    # Extract 'data' parameter if present
    data_dict = params.pop("data", None)

    for param_name, value in params.items():
        if value is None:
            continue

        # Convert snake_case to kebab-case for FortiOS API
        api_key = param_name.replace("_", "-")

        # Normalize list parameters if specified
        if param_name in fields_to_normalize:
            normalized = normalize_to_name_list(value)
            # Only add if normalization resulted in non-empty list
            if normalized:
                payload[api_key] = normalized
        else:
            payload[api_key] = value

    # Merge 'data' dictionary into payload (override existing keys)
    if data_dict and isinstance(data_dict, dict):
        payload.update(data_dict)

    return payload
