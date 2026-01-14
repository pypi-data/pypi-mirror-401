"""Type stubs for CMDB category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from . import alertemail
    from . import antivirus
    from . import application
    from . import authentication
    from . import automation
    from . import casb
    from . import certificate
    from . import diameter_filter
    from . import dlp
    from . import dnsfilter
    from . import emailfilter
    from . import endpoint_control
    from . import ethernet_oam
    from . import extension_controller
    from . import file_filter
    from . import firewall
    from . import ftp_proxy
    from . import icap
    from . import ips
    from . import log
    from . import monitoring
    from . import report
    from . import router
    from . import rule
    from . import sctp_filter
    from . import switch_controller
    from . import system
    from . import user
    from . import videofilter
    from . import virtual_patch
    from . import voip
    from . import vpn
    from . import waf
    from . import web_proxy
    from . import webfilter
    from . import wireless_controller
    from . import ztna

__all__ = [
    "CMDB",
    "CMDBDictMode",
    "CMDBObjectMode",
]

class CMDBDictMode:
    """CMDB API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    alertemail: alertemail.AlertemailDictMode
    antivirus: antivirus.AntivirusDictMode
    application: application.ApplicationDictMode
    authentication: authentication.AuthenticationDictMode
    automation: automation.AutomationDictMode
    casb: casb.CasbDictMode
    certificate: certificate.CertificateDictMode
    diameter_filter: diameter_filter.DiameterFilterDictMode
    dlp: dlp.DlpDictMode
    dnsfilter: dnsfilter.DnsfilterDictMode
    emailfilter: emailfilter.EmailfilterDictMode
    endpoint_control: endpoint_control.EndpointControlDictMode
    ethernet_oam: ethernet_oam.EthernetOamDictMode
    extension_controller: extension_controller.ExtensionControllerDictMode
    file_filter: file_filter.FileFilterDictMode
    firewall: firewall.FirewallDictMode
    ftp_proxy: ftp_proxy.FtpProxyDictMode
    icap: icap.IcapDictMode
    ips: ips.IpsDictMode
    log: log.LogDictMode
    monitoring: monitoring.MonitoringDictMode
    report: report.ReportDictMode
    router: router.RouterDictMode
    rule: rule.RuleDictMode
    sctp_filter: sctp_filter.SctpFilterDictMode
    switch_controller: switch_controller.SwitchControllerDictMode
    system: system.SystemDictMode
    user: user.UserDictMode
    videofilter: videofilter.VideofilterDictMode
    virtual_patch: virtual_patch.VirtualPatchDictMode
    voip: voip.VoipDictMode
    vpn: vpn.VpnDictMode
    waf: waf.WafDictMode
    web_proxy: web_proxy.WebProxyDictMode
    webfilter: webfilter.WebfilterDictMode
    wireless_controller: wireless_controller.WirelessControllerDictMode
    ztna: ztna.ZtnaDictMode

    def __init__(self, client: IHTTPClient) -> None:
        """Initialize CMDB category with HTTP client."""
        ...


class CMDBObjectMode:
    """CMDB API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    alertemail: alertemail.AlertemailObjectMode
    antivirus: antivirus.AntivirusObjectMode
    application: application.ApplicationObjectMode
    authentication: authentication.AuthenticationObjectMode
    automation: automation.AutomationObjectMode
    casb: casb.CasbObjectMode
    certificate: certificate.CertificateObjectMode
    diameter_filter: diameter_filter.DiameterFilterObjectMode
    dlp: dlp.DlpObjectMode
    dnsfilter: dnsfilter.DnsfilterObjectMode
    emailfilter: emailfilter.EmailfilterObjectMode
    endpoint_control: endpoint_control.EndpointControlObjectMode
    ethernet_oam: ethernet_oam.EthernetOamObjectMode
    extension_controller: extension_controller.ExtensionControllerObjectMode
    file_filter: file_filter.FileFilterObjectMode
    firewall: firewall.FirewallObjectMode
    ftp_proxy: ftp_proxy.FtpProxyObjectMode
    icap: icap.IcapObjectMode
    ips: ips.IpsObjectMode
    log: log.LogObjectMode
    monitoring: monitoring.MonitoringObjectMode
    report: report.ReportObjectMode
    router: router.RouterObjectMode
    rule: rule.RuleObjectMode
    sctp_filter: sctp_filter.SctpFilterObjectMode
    switch_controller: switch_controller.SwitchControllerObjectMode
    system: system.SystemObjectMode
    user: user.UserObjectMode
    videofilter: videofilter.VideofilterObjectMode
    virtual_patch: virtual_patch.VirtualPatchObjectMode
    voip: voip.VoipObjectMode
    vpn: vpn.VpnObjectMode
    waf: waf.WafObjectMode
    web_proxy: web_proxy.WebProxyObjectMode
    webfilter: webfilter.WebfilterObjectMode
    wireless_controller: wireless_controller.WirelessControllerObjectMode
    ztna: ztna.ZtnaObjectMode

    def __init__(self, client: IHTTPClient) -> None:
        """Initialize CMDB category with HTTP client."""
        ...


# Base class for backwards compatibility
class CMDB:
    """CMDB API category."""
    
    alertemail: alertemail.Alertemail
    antivirus: antivirus.Antivirus
    application: application.Application
    authentication: authentication.Authentication
    automation: automation.Automation
    casb: casb.Casb
    certificate: certificate.Certificate
    diameter_filter: diameter_filter.DiameterFilter
    dlp: dlp.Dlp
    dnsfilter: dnsfilter.Dnsfilter
    emailfilter: emailfilter.Emailfilter
    endpoint_control: endpoint_control.EndpointControl
    ethernet_oam: ethernet_oam.EthernetOam
    extension_controller: extension_controller.ExtensionController
    file_filter: file_filter.FileFilter
    firewall: firewall.Firewall
    ftp_proxy: ftp_proxy.FtpProxy
    icap: icap.Icap
    ips: ips.Ips
    log: log.Log
    monitoring: monitoring.Monitoring
    report: report.Report
    router: router.Router
    rule: rule.Rule
    sctp_filter: sctp_filter.SctpFilter
    switch_controller: switch_controller.SwitchController
    system: system.System
    user: user.User
    videofilter: videofilter.Videofilter
    virtual_patch: virtual_patch.VirtualPatch
    voip: voip.Voip
    vpn: vpn.Vpn
    waf: waf.Waf
    web_proxy: web_proxy.WebProxy
    webfilter: webfilter.Webfilter
    wireless_controller: wireless_controller.WirelessController
    ztna: ztna.Ztna

    def __init__(self, client: IHTTPClient) -> None:
        """Initialize CMDB category with HTTP client."""
        ...