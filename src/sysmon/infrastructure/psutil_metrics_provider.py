from typing import List

import psutil

from sysmon.domain.mountpoint_snapshot import MountPointSnapshot, MountPointMetrics
from sysmon.domain.system_snapshot import SystemSnapshot, CpuMetrics, MemoryMetrics


class PsutilMetricsProvider:
    def get_system_snapshot(self) -> SystemSnapshot:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent

        return SystemSnapshot(
            cpu=CpuMetrics(percent=cpu_percent),
            memory=MemoryMetrics(percent=memory_percent)
        )

    def get_mount_points_snapshot(self) -> List[MountPointSnapshot]:
        snapshots: list[MountPointSnapshot] = []

        for partition in psutil.disk_partitions(all=False):
            if "cdrom" in partition.opts or not partition.fstype:
                continue

            usage = psutil.disk_usage(partition.mountpoint)

            snapshot = MountPointSnapshot(
                mount_point=MountPointMetrics(
                    mount_point=partition.mountpoint,
                    capacity_bytes=usage.total,
                    free_bytes=usage.free,
                )
            )

            snapshots.append(snapshot)

        return snapshots