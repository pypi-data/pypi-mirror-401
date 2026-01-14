"""Type stubs for LOG category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .current_disk_usage import CurrentDiskUsage, CurrentDiskUsageDictMode, CurrentDiskUsageObjectMode
    from .feature_set import FeatureSet, FeatureSetDictMode, FeatureSetObjectMode
    from .fortianalyzer import Fortianalyzer, FortianalyzerDictMode, FortianalyzerObjectMode
    from .fortianalyzer_queue import FortianalyzerQueue, FortianalyzerQueueDictMode, FortianalyzerQueueObjectMode
    from .forticloud_report_list import ForticloudReportList, ForticloudReportListDictMode, ForticloudReportListObjectMode
    from .historic_daily_remote_logs import HistoricDailyRemoteLogs, HistoricDailyRemoteLogsDictMode, HistoricDailyRemoteLogsObjectMode
    from .hourly_disk_usage import HourlyDiskUsage, HourlyDiskUsageDictMode, HourlyDiskUsageObjectMode
    from .local_report_list import LocalReportList, LocalReportListDictMode, LocalReportListObjectMode
    from .av_archive import AvArchive
    from .device import DeviceDictMode, DeviceObjectMode
    from .forticloud import Forticloud
    from .forticloud_report import ForticloudReport
    from .local_report import LocalReport
    from .policy_archive import PolicyArchive
    from .stats import Stats

__all__ = [
    "CurrentDiskUsage",
    "FeatureSet",
    "Fortianalyzer",
    "FortianalyzerQueue",
    "ForticloudReportList",
    "HistoricDailyRemoteLogs",
    "HourlyDiskUsage",
    "LocalReportList",
    "LogDictMode",
    "LogObjectMode",
]

class LogDictMode:
    """LOG API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    av_archive: AvArchive
    device: DeviceDictMode
    forticloud: Forticloud
    forticloud_report: ForticloudReport
    local_report: LocalReport
    policy_archive: PolicyArchive
    stats: Stats
    current_disk_usage: CurrentDiskUsageDictMode
    feature_set: FeatureSetDictMode
    fortianalyzer: FortianalyzerDictMode
    fortianalyzer_queue: FortianalyzerQueueDictMode
    forticloud_report_list: ForticloudReportListDictMode
    historic_daily_remote_logs: HistoricDailyRemoteLogsDictMode
    hourly_disk_usage: HourlyDiskUsageDictMode
    local_report_list: LocalReportListDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize log category with HTTP client."""
        ...


class LogObjectMode:
    """LOG API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    av_archive: AvArchive
    device: DeviceObjectMode
    forticloud: Forticloud
    forticloud_report: ForticloudReport
    local_report: LocalReport
    policy_archive: PolicyArchive
    stats: Stats
    current_disk_usage: CurrentDiskUsageObjectMode
    feature_set: FeatureSetObjectMode
    fortianalyzer: FortianalyzerObjectMode
    fortianalyzer_queue: FortianalyzerQueueObjectMode
    forticloud_report_list: ForticloudReportListObjectMode
    historic_daily_remote_logs: HistoricDailyRemoteLogsObjectMode
    hourly_disk_usage: HourlyDiskUsageObjectMode
    local_report_list: LocalReportListObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize log category with HTTP client."""
        ...


# Base class for backwards compatibility
class Log:
    """LOG API category."""
    
    av_archive: AvArchive
    device: Device
    forticloud: Forticloud
    forticloud_report: ForticloudReport
    local_report: LocalReport
    policy_archive: PolicyArchive
    stats: Stats
    current_disk_usage: CurrentDiskUsage
    feature_set: FeatureSet
    fortianalyzer: Fortianalyzer
    fortianalyzer_queue: FortianalyzerQueue
    forticloud_report_list: ForticloudReportList
    historic_daily_remote_logs: HistoricDailyRemoteLogs
    hourly_disk_usage: HourlyDiskUsage
    local_report_list: LocalReportList

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize log category with HTTP client."""
        ...
