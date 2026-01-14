"""Type stubs for MCLAG_ICL category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .eligible_peer import EligiblePeer, EligiblePeerDictMode, EligiblePeerObjectMode
    from .set_tier1 import SetTier1, SetTier1DictMode, SetTier1ObjectMode
    from .set_tier_plus import SetTierPlus, SetTierPlusDictMode, SetTierPlusObjectMode
    from .tier_plus_candidates import TierPlusCandidates, TierPlusCandidatesDictMode, TierPlusCandidatesObjectMode

__all__ = [
    "EligiblePeer",
    "SetTier1",
    "SetTierPlus",
    "TierPlusCandidates",
    "MclagIclDictMode",
    "MclagIclObjectMode",
]

class MclagIclDictMode:
    """MCLAG_ICL API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    eligible_peer: EligiblePeerDictMode
    set_tier1: SetTier1DictMode
    set_tier_plus: SetTierPlusDictMode
    tier_plus_candidates: TierPlusCandidatesDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize mclag_icl category with HTTP client."""
        ...


class MclagIclObjectMode:
    """MCLAG_ICL API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    eligible_peer: EligiblePeerObjectMode
    set_tier1: SetTier1ObjectMode
    set_tier_plus: SetTierPlusObjectMode
    tier_plus_candidates: TierPlusCandidatesObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize mclag_icl category with HTTP client."""
        ...


# Base class for backwards compatibility
class MclagIcl:
    """MCLAG_ICL API category."""
    
    eligible_peer: EligiblePeer
    set_tier1: SetTier1
    set_tier_plus: SetTierPlus
    tier_plus_candidates: TierPlusCandidates

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize mclag_icl category with HTTP client."""
        ...
