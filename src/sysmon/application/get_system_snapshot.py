from sysmon.application.ports import MetricProvider
from sysmon.domain.system_snapshot import SystemSnapshot


# use case - what the program can do
class GetSystemSnapshot:
    def __init__(self, metrics_provider: MetricProvider):
        self.metrics_provider = metrics_provider

    def execute(self) -> SystemSnapshot:
        return self.metrics_provider.get_system_snapshot()