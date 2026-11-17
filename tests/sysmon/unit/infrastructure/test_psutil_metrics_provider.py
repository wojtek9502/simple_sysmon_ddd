from types import SimpleNamespace
from unittest.mock import patch

from sysmon.infrastructure.psutil_metrics_provider import PsutilMetricsProvider


PSUTIL_PATH = "sysmon.infrastructure.psutil_metrics_provider.psutil"


def test_get_system_snapshot_returns_cpu_and_memory_metrics():
    provider = PsutilMetricsProvider()

    with (
        patch(f"{PSUTIL_PATH}.cpu_percent", return_value=40.0) as cpu_percent,
        patch(
            f"{PSUTIL_PATH}.virtual_memory",
            return_value=SimpleNamespace(percent=60.0),
        ),
    ):
        snapshot = provider.get_system_snapshot()

    assert snapshot.cpu.percent == 40.0
    assert snapshot.memory.percent == 60.0


def test_get_mount_points_snapshot_returns_metrics_for_each_mount_point():
    provider = PsutilMetricsProvider()

    partitions = [
        SimpleNamespace(mountpoint="C:/", opts="rw", fstype="NTFS"),
        SimpleNamespace(mountpoint="D:/", opts="rw", fstype="NTFS"),
    ]

    with (
        patch(
            f"{PSUTIL_PATH}.disk_partitions",
            return_value=partitions,
        ) as disk_partitions,
        patch(
            f"{PSUTIL_PATH}.disk_usage",
            side_effect=[
                SimpleNamespace(total=1000, free=250),
                SimpleNamespace(total=2000, free=1000),
            ],
        ) as disk_usage,
    ):
        snapshots = provider.get_mount_points_snapshot()

    assert len(snapshots) == 2

    assert snapshots[0].mount_point.mount_point == "C:/"
    assert snapshots[0].mount_point.capacity_bytes == 1000
    assert snapshots[0].mount_point.free_bytes == 250

    assert snapshots[1].mount_point.mount_point == "D:/"
    assert snapshots[1].mount_point.capacity_bytes == 2000
    assert snapshots[1].mount_point.free_bytes == 1000

def test_get_mount_points_snapshot_skips_cdrom_and_missing_filesystem():
    provider = PsutilMetricsProvider()

    partitions = [
        SimpleNamespace(mountpoint="E:/", opts="ro,cdrom", fstype="CDFS"),
        SimpleNamespace(mountpoint="F:/", opts="rw", fstype=""),
    ]

    with (
        patch(
            f"{PSUTIL_PATH}.disk_partitions",
            return_value=partitions,
        ),
        patch(f"{PSUTIL_PATH}.disk_usage") as disk_usage,
    ):
        snapshots = provider.get_mount_points_snapshot()

    assert snapshots == []