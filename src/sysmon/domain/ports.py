from typing import Protocol, List

from sysmon.domain.mountpoint_snapshot import MountPointSnapshot
from sysmon.domain.system_snapshot import SystemSnapshot


# Contract. Done by Protocol to avoid inheritance
class MetricProvider(Protocol):
    def get_system_snapshot(self) -> SystemSnapshot:
        ...

    def get_mount_points_snapshot(self) -> List[MountPointSnapshot]:
        ...