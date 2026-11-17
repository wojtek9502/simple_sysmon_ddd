from sysmon.application.get_mount_points_snapshot import GetMountPointsSnapshot
from sysmon.application.get_system_snapshot import GetSystemSnapshot
from sysmon.infrastructure.psutil_metrics_provider import PsutilMetricsProvider


# composition root, here we select metric provider and run
def main():
    metrics_provider = PsutilMetricsProvider()
    system_snapshot = GetSystemSnapshot(metrics_provider=metrics_provider)
    system_snapshot_results = system_snapshot.execute()
    print(system_snapshot_results.overall_health())
    print(system_snapshot_results)

    mount_point_snapshot = GetMountPointsSnapshot(metrics_provider=metrics_provider)
    mount_point_snapshots_results = mount_point_snapshot.execute()
    for result in mount_point_snapshots_results:
        print(result.overall_health())
        print(result)



if __name__ == "__main__":
    main()