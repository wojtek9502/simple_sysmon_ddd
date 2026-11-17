from typing import List

from sysmon.application.get_system_snapshot import GetSystemSnapshot
from sysmon.domain.mountpoint_snapshot import MountPointSnapshot, MountPointMetrics
from sysmon.domain.system_snapshot import SystemSnapshot, CpuMetrics, MemoryMetrics
from tests.sysmon.unit.application import TEST_DISK_LABEL, TEST_DISC_CAPACITY, TEST_DISK_FREE


class FakeMetricsProvider:
    def get_system_snapshot(self) -> SystemSnapshot:
        return SystemSnapshot(
            cpu=CpuMetrics(percent=50.0),
            memory=MemoryMetrics(percent=60.0),
        )

    def get_mount_points_snapshot(self) -> List[MountPointSnapshot]:
        return [
                MountPointSnapshot(
                mount_point=MountPointMetrics(
                    mount_point=TEST_DISK_LABEL,
                    capacity_bytes=TEST_DISC_CAPACITY,
                    free_bytes=TEST_DISK_FREE

                ),
            )
        ]


def test_get_system_snapshot_returns_snapshot_from_provider():
    use_case = GetSystemSnapshot(metrics_provider=FakeMetricsProvider())
    snapshot = use_case.execute()

    assert snapshot.cpu.percent == 50.0
    assert snapshot.memory.percent == 60.0
