"""Type stubs for HOTSPOT20 category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .anqp_3gpp_cellular import Anqp3gppCellular, Anqp3gppCellularDictMode, Anqp3gppCellularObjectMode
    from .anqp_ip_address_type import AnqpIpAddressType, AnqpIpAddressTypeDictMode, AnqpIpAddressTypeObjectMode
    from .anqp_nai_realm import AnqpNaiRealm, AnqpNaiRealmDictMode, AnqpNaiRealmObjectMode
    from .anqp_network_auth_type import AnqpNetworkAuthType, AnqpNetworkAuthTypeDictMode, AnqpNetworkAuthTypeObjectMode
    from .anqp_roaming_consortium import AnqpRoamingConsortium, AnqpRoamingConsortiumDictMode, AnqpRoamingConsortiumObjectMode
    from .anqp_venue_name import AnqpVenueName, AnqpVenueNameDictMode, AnqpVenueNameObjectMode
    from .anqp_venue_url import AnqpVenueUrl, AnqpVenueUrlDictMode, AnqpVenueUrlObjectMode
    from .h2qp_advice_of_charge import H2qpAdviceOfCharge, H2qpAdviceOfChargeDictMode, H2qpAdviceOfChargeObjectMode
    from .h2qp_conn_capability import H2qpConnCapability, H2qpConnCapabilityDictMode, H2qpConnCapabilityObjectMode
    from .h2qp_operator_name import H2qpOperatorName, H2qpOperatorNameDictMode, H2qpOperatorNameObjectMode
    from .h2qp_osu_provider import H2qpOsuProvider, H2qpOsuProviderDictMode, H2qpOsuProviderObjectMode
    from .h2qp_osu_provider_nai import H2qpOsuProviderNai, H2qpOsuProviderNaiDictMode, H2qpOsuProviderNaiObjectMode
    from .h2qp_terms_and_conditions import H2qpTermsAndConditions, H2qpTermsAndConditionsDictMode, H2qpTermsAndConditionsObjectMode
    from .h2qp_wan_metric import H2qpWanMetric, H2qpWanMetricDictMode, H2qpWanMetricObjectMode
    from .hs_profile import HsProfile, HsProfileDictMode, HsProfileObjectMode
    from .icon import Icon, IconDictMode, IconObjectMode
    from .qos_map import QosMap, QosMapDictMode, QosMapObjectMode

__all__ = [
    "Anqp3gppCellular",
    "AnqpIpAddressType",
    "AnqpNaiRealm",
    "AnqpNetworkAuthType",
    "AnqpRoamingConsortium",
    "AnqpVenueName",
    "AnqpVenueUrl",
    "H2qpAdviceOfCharge",
    "H2qpConnCapability",
    "H2qpOperatorName",
    "H2qpOsuProvider",
    "H2qpOsuProviderNai",
    "H2qpTermsAndConditions",
    "H2qpWanMetric",
    "HsProfile",
    "Icon",
    "QosMap",
    "Hotspot20DictMode",
    "Hotspot20ObjectMode",
]

class Hotspot20DictMode:
    """HOTSPOT20 API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    anqp_3gpp_cellular: Anqp3gppCellularDictMode
    anqp_ip_address_type: AnqpIpAddressTypeDictMode
    anqp_nai_realm: AnqpNaiRealmDictMode
    anqp_network_auth_type: AnqpNetworkAuthTypeDictMode
    anqp_roaming_consortium: AnqpRoamingConsortiumDictMode
    anqp_venue_name: AnqpVenueNameDictMode
    anqp_venue_url: AnqpVenueUrlDictMode
    h2qp_advice_of_charge: H2qpAdviceOfChargeDictMode
    h2qp_conn_capability: H2qpConnCapabilityDictMode
    h2qp_operator_name: H2qpOperatorNameDictMode
    h2qp_osu_provider: H2qpOsuProviderDictMode
    h2qp_osu_provider_nai: H2qpOsuProviderNaiDictMode
    h2qp_terms_and_conditions: H2qpTermsAndConditionsDictMode
    h2qp_wan_metric: H2qpWanMetricDictMode
    hs_profile: HsProfileDictMode
    icon: IconDictMode
    qos_map: QosMapDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize hotspot20 category with HTTP client."""
        ...


class Hotspot20ObjectMode:
    """HOTSPOT20 API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    anqp_3gpp_cellular: Anqp3gppCellularObjectMode
    anqp_ip_address_type: AnqpIpAddressTypeObjectMode
    anqp_nai_realm: AnqpNaiRealmObjectMode
    anqp_network_auth_type: AnqpNetworkAuthTypeObjectMode
    anqp_roaming_consortium: AnqpRoamingConsortiumObjectMode
    anqp_venue_name: AnqpVenueNameObjectMode
    anqp_venue_url: AnqpVenueUrlObjectMode
    h2qp_advice_of_charge: H2qpAdviceOfChargeObjectMode
    h2qp_conn_capability: H2qpConnCapabilityObjectMode
    h2qp_operator_name: H2qpOperatorNameObjectMode
    h2qp_osu_provider: H2qpOsuProviderObjectMode
    h2qp_osu_provider_nai: H2qpOsuProviderNaiObjectMode
    h2qp_terms_and_conditions: H2qpTermsAndConditionsObjectMode
    h2qp_wan_metric: H2qpWanMetricObjectMode
    hs_profile: HsProfileObjectMode
    icon: IconObjectMode
    qos_map: QosMapObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize hotspot20 category with HTTP client."""
        ...


# Base class for backwards compatibility
class Hotspot20:
    """HOTSPOT20 API category."""
    
    anqp_3gpp_cellular: Anqp3gppCellular
    anqp_ip_address_type: AnqpIpAddressType
    anqp_nai_realm: AnqpNaiRealm
    anqp_network_auth_type: AnqpNetworkAuthType
    anqp_roaming_consortium: AnqpRoamingConsortium
    anqp_venue_name: AnqpVenueName
    anqp_venue_url: AnqpVenueUrl
    h2qp_advice_of_charge: H2qpAdviceOfCharge
    h2qp_conn_capability: H2qpConnCapability
    h2qp_operator_name: H2qpOperatorName
    h2qp_osu_provider: H2qpOsuProvider
    h2qp_osu_provider_nai: H2qpOsuProviderNai
    h2qp_terms_and_conditions: H2qpTermsAndConditions
    h2qp_wan_metric: H2qpWanMetric
    hs_profile: HsProfile
    icon: Icon
    qos_map: QosMap

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize hotspot20 category with HTTP client."""
        ...
