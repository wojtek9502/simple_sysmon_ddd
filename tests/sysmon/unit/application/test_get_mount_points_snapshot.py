from typing import List

from sysmon.application.get_mount_points_snapshot import GetMountPointsSnapshot
from sysmon.domain.mountpoint_snapshot import MountPointSnapshot, MountPointMetrics
from sysmon.domain.system_snapshot import SystemSnapshot, CpuMetrics, MemoryMetrics
from tests.sysmon.unit.application import TEST_DISK_LABEL, TEST_DISC_CAPACITY, TEST_DISK_FREE, TEST_DISK_USED, \
    TEST_DISK_USAGE_PERCENT


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


def test_get_mount_point_snapshot_returns_snapshot_from_provider():
    use_case = GetMountPointsSnapshot(metrics_provider=FakeMetricsProvider())
    mount_points_snapshot = use_case.execute()

    assert mount_points_snapshot[0].mount_point.mount_point == TEST_DISK_LABEL
    assert mount_points_snapshot[0].mount_point.capacity_bytes == TEST_DISC_CAPACITY
    assert mount_points_snapshot[0].mount_point.used_bytes == TEST_DISK_USED
    assert mount_points_snapshot[0].mount_point.free_bytes == TEST_DISK_FREE
    assert mount_points_snapshot[0].mount_point.usage_percent == TEST_DISK_USAGE_PERCENT