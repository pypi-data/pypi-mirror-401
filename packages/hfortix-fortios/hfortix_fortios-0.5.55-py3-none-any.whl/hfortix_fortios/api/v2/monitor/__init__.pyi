"""Type stubs for MONITOR category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from . import azure
    from . import casb
    from . import endpoint_control
    from . import extender_controller
    from . import extension_controller
    from . import firewall
    from . import firmware
    from . import fortiguard
    from . import fortiview
    from . import geoip
    from . import ips
    from . import license
    from . import log
    from . import network
    from . import registration
    from . import router
    from . import sdwan
    from . import service
    from . import switch_controller
    from . import system
    from . import user
    from . import utm
    from . import videofilter
    from . import virtual_wan
    from . import vpn
    from . import vpn_certificate
    from . import wanopt
    from . import web_ui
    from . import webcache
    from . import webfilter
    from . import webproxy
    from . import wifi

__all__ = [
    "MONITOR",
    "MONITORDictMode",
    "MONITORObjectMode",
]

class MONITORDictMode:
    """MONITOR API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    azure: azure.AzureDictMode
    casb: casb.CasbDictMode
    endpoint_control: endpoint_control.EndpointControl  # No mode classes yet
    extender_controller: extender_controller.ExtenderController  # No mode classes yet
    extension_controller: extension_controller.ExtensionController  # No mode classes yet
    firewall: firewall.FirewallDictMode
    firmware: firmware.FirmwareDictMode
    fortiguard: fortiguard.FortiguardDictMode
    fortiview: fortiview.FortiviewDictMode
    geoip: geoip.GeoipDictMode
    ips: ips.IpsDictMode
    license: license.LicenseDictMode
    log: log.LogDictMode
    network: network.NetworkDictMode
    registration: registration.RegistrationDictMode
    router: router.RouterDictMode
    sdwan: sdwan.SdwanDictMode
    service: service.ServiceDictMode
    switch_controller: switch_controller.SwitchController  # No mode classes yet
    system: system.SystemDictMode
    user: user.UserDictMode
    utm: utm.UtmDictMode
    videofilter: videofilter.VideofilterDictMode
    virtual_wan: virtual_wan.VirtualWan  # No mode classes yet
    vpn: vpn.VpnDictMode
    vpn_certificate: vpn_certificate.VpnCertificate  # No mode classes yet
    wanopt: wanopt.WanoptDictMode
    web_ui: web_ui.WebUi  # No mode classes yet
    webcache: webcache.WebcacheDictMode
    webfilter: webfilter.WebfilterDictMode
    webproxy: webproxy.WebproxyDictMode
    wifi: wifi.WifiDictMode

    def __init__(self, client: IHTTPClient) -> None:
        """Initialize MONITOR category with HTTP client."""
        ...


class MONITORObjectMode:
    """MONITOR API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    azure: azure.AzureObjectMode
    casb: casb.CasbObjectMode
    endpoint_control: endpoint_control.EndpointControl  # No mode classes yet
    extender_controller: extender_controller.ExtenderController  # No mode classes yet
    extension_controller: extension_controller.ExtensionController  # No mode classes yet
    firewall: firewall.FirewallObjectMode
    firmware: firmware.FirmwareObjectMode
    fortiguard: fortiguard.FortiguardObjectMode
    fortiview: fortiview.FortiviewObjectMode
    geoip: geoip.GeoipObjectMode
    ips: ips.IpsObjectMode
    license: license.LicenseObjectMode
    log: log.LogObjectMode
    network: network.NetworkObjectMode
    registration: registration.RegistrationObjectMode
    router: router.RouterObjectMode
    sdwan: sdwan.SdwanObjectMode
    service: service.ServiceObjectMode
    switch_controller: switch_controller.SwitchController  # No mode classes yet
    system: system.SystemObjectMode
    user: user.UserObjectMode
    utm: utm.UtmObjectMode
    videofilter: videofilter.VideofilterObjectMode
    virtual_wan: virtual_wan.VirtualWan  # No mode classes yet
    vpn: vpn.VpnObjectMode
    vpn_certificate: vpn_certificate.VpnCertificate  # No mode classes yet
    wanopt: wanopt.WanoptObjectMode
    web_ui: web_ui.WebUi  # No mode classes yet
    webcache: webcache.WebcacheObjectMode
    webfilter: webfilter.WebfilterObjectMode
    webproxy: webproxy.WebproxyObjectMode
    wifi: wifi.WifiObjectMode

    def __init__(self, client: IHTTPClient) -> None:
        """Initialize MONITOR category with HTTP client."""
        ...


# Base class for backwards compatibility
class MONITOR:
    """MONITOR API category."""
    
    azure: azure.Azure
    casb: casb.Casb
    endpoint_control: endpoint_control.EndpointControl
    extender_controller: extender_controller.ExtenderController
    extension_controller: extension_controller.ExtensionController
    firewall: firewall.Firewall
    firmware: firmware.Firmware
    fortiguard: fortiguard.Fortiguard
    fortiview: fortiview.Fortiview
    geoip: geoip.Geoip
    ips: ips.Ips
    license: license.License
    log: log.Log
    network: network.Network
    registration: registration.Registration
    router: router.Router
    sdwan: sdwan.Sdwan
    service: service.Service
    switch_controller: switch_controller.SwitchController
    system: system.System
    user: user.User
    utm: utm.Utm
    videofilter: videofilter.Videofilter
    virtual_wan: virtual_wan.VirtualWan
    vpn: vpn.Vpn
    vpn_certificate: vpn_certificate.VpnCertificate
    wanopt: wanopt.Wanopt
    web_ui: web_ui.WebUi
    webcache: webcache.Webcache
    webfilter: webfilter.Webfilter
    webproxy: webproxy.Webproxy
    wifi: wifi.Wifi

    def __init__(self, client: IHTTPClient) -> None:
        """Initialize MONITOR category with HTTP client."""
        ...