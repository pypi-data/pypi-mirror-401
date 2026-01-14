"""Type stubs for USER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .adgrp import Adgrp, AdgrpDictMode, AdgrpObjectMode
    from .certificate import Certificate, CertificateDictMode, CertificateObjectMode
    from .domain_controller import DomainController, DomainControllerDictMode, DomainControllerObjectMode
    from .exchange import Exchange, ExchangeDictMode, ExchangeObjectMode
    from .external_identity_provider import ExternalIdentityProvider, ExternalIdentityProviderDictMode, ExternalIdentityProviderObjectMode
    from .fortitoken import Fortitoken, FortitokenDictMode, FortitokenObjectMode
    from .fsso import Fsso, FssoDictMode, FssoObjectMode
    from .fsso_polling import FssoPolling, FssoPollingDictMode, FssoPollingObjectMode
    from .group import Group, GroupDictMode, GroupObjectMode
    from .krb_keytab import KrbKeytab, KrbKeytabDictMode, KrbKeytabObjectMode
    from .ldap import Ldap, LdapDictMode, LdapObjectMode
    from .local import Local, LocalDictMode, LocalObjectMode
    from .nac_policy import NacPolicy, NacPolicyDictMode, NacPolicyObjectMode
    from .password_policy import PasswordPolicy, PasswordPolicyDictMode, PasswordPolicyObjectMode
    from .peer import Peer, PeerDictMode, PeerObjectMode
    from .peergrp import Peergrp, PeergrpDictMode, PeergrpObjectMode
    from .pop3 import Pop3, Pop3DictMode, Pop3ObjectMode
    from .quarantine import Quarantine, QuarantineDictMode, QuarantineObjectMode
    from .radius import Radius, RadiusDictMode, RadiusObjectMode
    from .saml import Saml, SamlDictMode, SamlObjectMode
    from .scim import Scim, ScimDictMode, ScimObjectMode
    from .security_exempt_list import SecurityExemptList, SecurityExemptListDictMode, SecurityExemptListObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode
    from .tacacs_plus import TacacsPlus, TacacsPlusDictMode, TacacsPlusObjectMode

__all__ = [
    "Adgrp",
    "Certificate",
    "DomainController",
    "Exchange",
    "ExternalIdentityProvider",
    "Fortitoken",
    "Fsso",
    "FssoPolling",
    "Group",
    "KrbKeytab",
    "Ldap",
    "Local",
    "NacPolicy",
    "PasswordPolicy",
    "Peer",
    "Peergrp",
    "Pop3",
    "Quarantine",
    "Radius",
    "Saml",
    "Scim",
    "SecurityExemptList",
    "Setting",
    "TacacsPlus",
    "UserDictMode",
    "UserObjectMode",
]

class UserDictMode:
    """USER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    adgrp: AdgrpDictMode
    certificate: CertificateDictMode
    domain_controller: DomainControllerDictMode
    exchange: ExchangeDictMode
    external_identity_provider: ExternalIdentityProviderDictMode
    fortitoken: FortitokenDictMode
    fsso: FssoDictMode
    fsso_polling: FssoPollingDictMode
    group: GroupDictMode
    krb_keytab: KrbKeytabDictMode
    ldap: LdapDictMode
    local: LocalDictMode
    nac_policy: NacPolicyDictMode
    password_policy: PasswordPolicyDictMode
    peer: PeerDictMode
    peergrp: PeergrpDictMode
    pop3: Pop3DictMode
    quarantine: QuarantineDictMode
    radius: RadiusDictMode
    saml: SamlDictMode
    scim: ScimDictMode
    security_exempt_list: SecurityExemptListDictMode
    setting: SettingDictMode
    tacacs_plus: TacacsPlusDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize user category with HTTP client."""
        ...


class UserObjectMode:
    """USER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    adgrp: AdgrpObjectMode
    certificate: CertificateObjectMode
    domain_controller: DomainControllerObjectMode
    exchange: ExchangeObjectMode
    external_identity_provider: ExternalIdentityProviderObjectMode
    fortitoken: FortitokenObjectMode
    fsso: FssoObjectMode
    fsso_polling: FssoPollingObjectMode
    group: GroupObjectMode
    krb_keytab: KrbKeytabObjectMode
    ldap: LdapObjectMode
    local: LocalObjectMode
    nac_policy: NacPolicyObjectMode
    password_policy: PasswordPolicyObjectMode
    peer: PeerObjectMode
    peergrp: PeergrpObjectMode
    pop3: Pop3ObjectMode
    quarantine: QuarantineObjectMode
    radius: RadiusObjectMode
    saml: SamlObjectMode
    scim: ScimObjectMode
    security_exempt_list: SecurityExemptListObjectMode
    setting: SettingObjectMode
    tacacs_plus: TacacsPlusObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize user category with HTTP client."""
        ...


# Base class for backwards compatibility
class User:
    """USER API category."""
    
    adgrp: Adgrp
    certificate: Certificate
    domain_controller: DomainController
    exchange: Exchange
    external_identity_provider: ExternalIdentityProvider
    fortitoken: Fortitoken
    fsso: Fsso
    fsso_polling: FssoPolling
    group: Group
    krb_keytab: KrbKeytab
    ldap: Ldap
    local: Local
    nac_policy: NacPolicy
    password_policy: PasswordPolicy
    peer: Peer
    peergrp: Peergrp
    pop3: Pop3
    quarantine: Quarantine
    radius: Radius
    saml: Saml
    scim: Scim
    security_exempt_list: SecurityExemptList
    setting: Setting
    tacacs_plus: TacacsPlus

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize user category with HTTP client."""
        ...
