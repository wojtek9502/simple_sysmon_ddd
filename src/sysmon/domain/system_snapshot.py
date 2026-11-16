from dataclasses import dataclass
from enum import Enum

CPU_PERCENT_WARNING_THRESHOLD = 75
MEMORY_PERCENT_WARNING_THRESHOLD = 75
CPU_PERCENT_CRITICAL_THRESHOLD = 90
MEMORY_PERCENT_CRITICAL_THRESHOLD = 90

# Domain model
class HealthStatus(Enum):
    OK = 'ok'
    WARNING = 'warning'
    CRITICAL = 'critical'

# Value Object
@dataclass(frozen=True)
class CpuMetrics:
    percent: float

# Value Object
@dataclass(frozen=True)
class MemoryMetrics:
    percent: float


# Aggregate root
@dataclass(frozen=True)
class SystemSnapshot:
    cpu: CpuMetrics
    memory: MemoryMetrics

    # business rule
    def overall_health(self) -> HealthStatus:
        if self.cpu.percent >= CPU_PERCENT_CRITICAL_THRESHOLD or self.memory.percent >= MEMORY_PERCENT_CRITICAL_THRESHOLD:
            return HealthStatus.CRITICAL

        if self.cpu.percent >= CPU_PERCENT_WARNING_THRESHOLD or self.memory.percent >= MEMORY_PERCENT_WARNING_THRESHOLD:
            return HealthStatus.WARNING

        return HealthStatus.OK