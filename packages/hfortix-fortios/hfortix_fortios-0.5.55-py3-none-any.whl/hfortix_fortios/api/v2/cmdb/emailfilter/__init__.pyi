"""Type stubs for EMAILFILTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .block_allow_list import BlockAllowList, BlockAllowListDictMode, BlockAllowListObjectMode
    from .bword import Bword, BwordDictMode, BwordObjectMode
    from .dnsbl import Dnsbl, DnsblDictMode, DnsblObjectMode
    from .fortishield import Fortishield, FortishieldDictMode, FortishieldObjectMode
    from .iptrust import Iptrust, IptrustDictMode, IptrustObjectMode
    from .mheader import Mheader, MheaderDictMode, MheaderObjectMode
    from .options import Options, OptionsDictMode, OptionsObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode

__all__ = [
    "BlockAllowList",
    "Bword",
    "Dnsbl",
    "Fortishield",
    "Iptrust",
    "Mheader",
    "Options",
    "Profile",
    "EmailfilterDictMode",
    "EmailfilterObjectMode",
]

class EmailfilterDictMode:
    """EMAILFILTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    block_allow_list: BlockAllowListDictMode
    bword: BwordDictMode
    dnsbl: DnsblDictMode
    fortishield: FortishieldDictMode
    iptrust: IptrustDictMode
    mheader: MheaderDictMode
    options: OptionsDictMode
    profile: ProfileDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize emailfilter category with HTTP client."""
        ...


class EmailfilterObjectMode:
    """EMAILFILTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    block_allow_list: BlockAllowListObjectMode
    bword: BwordObjectMode
    dnsbl: DnsblObjectMode
    fortishield: FortishieldObjectMode
    iptrust: IptrustObjectMode
    mheader: MheaderObjectMode
    options: OptionsObjectMode
    profile: ProfileObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize emailfilter category with HTTP client."""
        ...


# Base class for backwards compatibility
class Emailfilter:
    """EMAILFILTER API category."""
    
    block_allow_list: BlockAllowList
    bword: Bword
    dnsbl: Dnsbl
    fortishield: Fortishield
    iptrust: Iptrust
    mheader: Mheader
    options: Options
    profile: Profile

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize emailfilter category with HTTP client."""
        ...
