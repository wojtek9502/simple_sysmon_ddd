import pytest

from src.sysmon.domain.mountpoint_snapshot import (
    MountPointMetrics,
    MountPointSnapshot,
    HealthStatus
)

def test_mount_point_snapshot_is_ok_when_mount_point_usage_is_below_warning_threshold():
    snapshot = MountPointSnapshot(
        mount_point=MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=260,
        )
    )

    assert snapshot.overall_health() == HealthStatus.OK


def test_mount_point_snapshot_is_warning_when_mount_point_usage_is_exactly_75_percent():
    snapshot = MountPointSnapshot(
        mount_point=MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=250,
        )
    )

    assert snapshot.overall_health() == HealthStatus.WARNING


def test_mount_point_snapshot_is_warning_when_mount_point_usage_is_below_critical_threshold():
    snapshot = MountPointSnapshot(
        mount_point=MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=110,
        )
    )

    assert snapshot.overall_health() == HealthStatus.WARNING


def test_mount_point_snapshot_is_critical_when_mount_point_usage_is_exactly_90_percent():
    snapshot = MountPointSnapshot(
        mount_point=MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=100,
        )
    )

    assert snapshot.overall_health() == HealthStatus.CRITICAL


def test_mount_point_snapshot_is_ok_when_mount_point_is_empty():
    snapshot = MountPointSnapshot(
        mount_point=MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=1000,
        )
    )

    assert snapshot.overall_health() == HealthStatus.OK


def test_mount_point_snapshot_is_critical_when_mount_point_is_full():
    snapshot = MountPointSnapshot(
        mount_point=MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=0,
        )
    )

    assert snapshot.overall_health() == HealthStatus.CRITICAL

def test_mount_point_metrics_calculates_used_bytes():
    mount_point = MountPointMetrics(
        mount_point="C:\\",
        capacity_bytes=1000,
        free_bytes=250,
    )

    assert mount_point.used_bytes == 750


def test_mount_point_metrics_calculates_usage_percent():
    mount_point = MountPointMetrics(
        mount_point="C:\\",
        capacity_bytes=1000,
        free_bytes=250,
    )

    assert mount_point.usage_percent == 75.0


def test_mount_point_metrics_calculates_fractional_usage_percent():
    mount_point = MountPointMetrics(
        mount_point="C:\\",
        capacity_bytes=1024,
        free_bytes=8,
    )

    assert mount_point.usage_percent == pytest.approx(99.21875)


def test_mount_point_metrics_usage_percent_is_zero_when_mount_point_is_empty():
    mount_point = MountPointMetrics(
        mount_point="C:\\",
        capacity_bytes=1000,
        free_bytes=1000,
    )

    assert mount_point.usage_percent == 0.0


def test_mount_point_metrics_usage_percent_is_100_when_mount_point_is_full():
    mount_point = MountPointMetrics(
        mount_point="C:\\",
        capacity_bytes=1000,
        free_bytes=0,
    )

    assert mount_point.usage_percent == 100.0

def test_mount_point_metrics_rejects_zero_capacity():
    with pytest.raises(ValueError):
        MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=0,
            free_bytes=0,
        )


def test_mount_point_metrics_rejects_negative_capacity():
    with pytest.raises(ValueError):
        MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=-1000,
            free_bytes=0,
        )


def test_mount_point_metrics_rejects_negative_free_bytes():
    with pytest.raises(ValueError):
        MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=-1,
        )


def test_mount_point_metrics_rejects_free_bytes_greater_than_capacity():
    with pytest.raises(ValueError):
        MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=1001,
        )

def test_mount_point_snapshot_repr():
    snapshot = MountPointSnapshot(
        mount_point=MountPointMetrics(
            mount_point="C:\\",
            capacity_bytes=1000,
            free_bytes=260,
        )
    )

    assert "Mount point: C:\\ Bytes: 1000 Free: 260" in snapshot.__repr__()
