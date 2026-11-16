# tests/unit/test_system_snapshot.py
from src.sysmon.domain.system_snapshot import (
    CPU_PERCENT_CRITICAL_THRESHOLD,
    CPU_PERCENT_WARNING_THRESHOLD,
    MEMORY_PERCENT_CRITICAL_THRESHOLD,
    MEMORY_PERCENT_WARNING_THRESHOLD,
    CpuMetrics,
    HealthStatus,
    MemoryMetrics,
    SystemSnapshot,
)


def test_system_snapshot_is_ok_when_cpu_and_memory_are_low():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=20.0),
        memory=MemoryMetrics(percent=30.0),
    )

    assert snapshot.overall_health() == HealthStatus.OK


def test_system_snapshot_is_ok_when_cpu_and_memory_are_below_warning_threshold():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=CPU_PERCENT_WARNING_THRESHOLD - 0.1),
        memory=MemoryMetrics(percent=MEMORY_PERCENT_WARNING_THRESHOLD - 0.1),
    )

    assert snapshot.overall_health() == HealthStatus.OK


def test_system_snapshot_is_warning_when_cpu_is_low_and_memory_is_medium():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=20.0),
        memory=MemoryMetrics(percent=80.0),
    )

    assert snapshot.overall_health() == HealthStatus.WARNING


def test_system_snapshot_is_warning_when_cpu_is_medium_and_memory_is_low():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=80.0),
        memory=MemoryMetrics(percent=20.0),
    )

    assert snapshot.overall_health() == HealthStatus.WARNING


def test_system_snapshot_is_warning_when_cpu_is_medium_and_memory_is_medium():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=80.0),
        memory=MemoryMetrics(percent=80.0),
    )

    assert snapshot.overall_health() == HealthStatus.WARNING


def test_system_snapshot_is_warning_when_cpu_is_on_warning_threshold():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=CPU_PERCENT_WARNING_THRESHOLD),
        memory=MemoryMetrics(percent=20.0),
    )

    assert snapshot.overall_health() == HealthStatus.WARNING


def test_system_snapshot_is_warning_when_memory_is_on_warning_threshold():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=20.0),
        memory=MemoryMetrics(percent=MEMORY_PERCENT_WARNING_THRESHOLD),
    )

    assert snapshot.overall_health() == HealthStatus.WARNING


def test_system_snapshot_is_warning_when_cpu_and_memory_are_on_warning_threshold():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=CPU_PERCENT_WARNING_THRESHOLD),
        memory=MemoryMetrics(percent=MEMORY_PERCENT_WARNING_THRESHOLD),
    )

    assert snapshot.overall_health() == HealthStatus.WARNING


def test_system_snapshot_is_critical_when_cpu_is_on_critical_threshold():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=CPU_PERCENT_CRITICAL_THRESHOLD),
        memory=MemoryMetrics(percent=20.0),
    )

    assert snapshot.overall_health() == HealthStatus.CRITICAL


def test_system_snapshot_is_critical_when_memory_is_on_critical_threshold():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=20.0),
        memory=MemoryMetrics(percent=MEMORY_PERCENT_CRITICAL_THRESHOLD),
    )

    assert snapshot.overall_health() == HealthStatus.CRITICAL


def test_system_snapshot_is_critical_when_cpu_and_memory_are_on_critical_threshold():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=CPU_PERCENT_CRITICAL_THRESHOLD),
        memory=MemoryMetrics(percent=MEMORY_PERCENT_CRITICAL_THRESHOLD),
    )

    assert snapshot.overall_health() == HealthStatus.CRITICAL


def test_system_snapshot_is_critical_when_cpu_is_very_high():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=95.0),
        memory=MemoryMetrics(percent=20.0),
    )

    assert snapshot.overall_health() == HealthStatus.CRITICAL


def test_system_snapshot_is_critical_when_memory_is_very_high():
    snapshot = SystemSnapshot(
        cpu=CpuMetrics(percent=20.0),
        memory=MemoryMetrics(percent=95.0),
    )

    assert snapshot.overall_health() == HealthStatus.CRITICAL


def test_warning_threshold_is_75_percent():
    assert CPU_PERCENT_WARNING_THRESHOLD == 75
    assert MEMORY_PERCENT_WARNING_THRESHOLD == 75


def test_critical_threshold_is_90_percent():
    assert CPU_PERCENT_CRITICAL_THRESHOLD == 90
    assert MEMORY_PERCENT_CRITICAL_THRESHOLD == 90