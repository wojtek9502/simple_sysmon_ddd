from typing import List

from sysmon.domain.mountpoint_snapshot import MountPointSnapshot
from sysmon.application.ports import MetricProvider


class GetMountPointsSnapshot:
    def __init__(self, metrics_provider: MetricProvider):
        self.metrics_provider = metrics_provider

    def execute(self) -> List[MountPointSnapshot]:
        return self.metrics_provider.get_mount_points_snapshot()