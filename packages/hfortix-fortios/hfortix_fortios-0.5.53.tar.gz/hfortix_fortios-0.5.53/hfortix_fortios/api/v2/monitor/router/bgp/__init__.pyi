"""Type stubs for BGP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .clear_soft_in import ClearSoftIn, ClearSoftInDictMode, ClearSoftInObjectMode
    from .clear_soft_out import ClearSoftOut, ClearSoftOutDictMode, ClearSoftOutObjectMode
    from .neighbors import Neighbors, NeighborsDictMode, NeighborsObjectMode
    from .neighbors6 import Neighbors6, Neighbors6DictMode, Neighbors6ObjectMode
    from .neighbors_statistics import NeighborsStatistics, NeighborsStatisticsDictMode, NeighborsStatisticsObjectMode
    from .paths import Paths, PathsDictMode, PathsObjectMode
    from .paths6 import Paths6, Paths6DictMode, Paths6ObjectMode
    from .paths_statistics import PathsStatistics, PathsStatisticsDictMode, PathsStatisticsObjectMode
    from .soft_reset_neighbor import SoftResetNeighbor, SoftResetNeighborDictMode, SoftResetNeighborObjectMode

__all__ = [
    "ClearSoftIn",
    "ClearSoftOut",
    "Neighbors",
    "Neighbors6",
    "NeighborsStatistics",
    "Paths",
    "Paths6",
    "PathsStatistics",
    "SoftResetNeighbor",
    "BgpDictMode",
    "BgpObjectMode",
]

class BgpDictMode:
    """BGP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    clear_soft_in: ClearSoftInDictMode
    clear_soft_out: ClearSoftOutDictMode
    neighbors: NeighborsDictMode
    neighbors6: Neighbors6DictMode
    neighbors_statistics: NeighborsStatisticsDictMode
    paths: PathsDictMode
    paths6: Paths6DictMode
    paths_statistics: PathsStatisticsDictMode
    soft_reset_neighbor: SoftResetNeighborDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize bgp category with HTTP client."""
        ...


class BgpObjectMode:
    """BGP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    clear_soft_in: ClearSoftInObjectMode
    clear_soft_out: ClearSoftOutObjectMode
    neighbors: NeighborsObjectMode
    neighbors6: Neighbors6ObjectMode
    neighbors_statistics: NeighborsStatisticsObjectMode
    paths: PathsObjectMode
    paths6: Paths6ObjectMode
    paths_statistics: PathsStatisticsObjectMode
    soft_reset_neighbor: SoftResetNeighborObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize bgp category with HTTP client."""
        ...


# Base class for backwards compatibility
class Bgp:
    """BGP API category."""
    
    clear_soft_in: ClearSoftIn
    clear_soft_out: ClearSoftOut
    neighbors: Neighbors
    neighbors6: Neighbors6
    neighbors_statistics: NeighborsStatistics
    paths: Paths
    paths6: Paths6
    paths_statistics: PathsStatistics
    soft_reset_neighbor: SoftResetNeighbor

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize bgp category with HTTP client."""
        ...
