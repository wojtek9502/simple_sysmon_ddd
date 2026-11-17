from dataclasses import dataclass
from enum import Enum

DISK_PERCENT_CRITICAL_THRESHOLD = 90.0
DISK_PERCENT_WARNING_THRESHOLD = 75.0

# Domain model
class HealthStatus(Enum):
    OK = 'ok'
    WARNING = 'warning'
    CRITICAL = 'critical'

# Value Object
@dataclass(frozen=True)
class MountPointMetrics:
    mount_point: str
    capacity_bytes: int
    free_bytes: int

    @property
    def used_bytes(self) -> int:
        return self.capacity_bytes - self.free_bytes

    @property
    def usage_percent(self) -> float:
        return self.used_bytes / self.capacity_bytes * 100

    def __post_init__(self) -> None:
        if self.capacity_bytes <= 0:
            raise ValueError("capacity_bytes must be greater than zero")

        if not 0 <= self.free_bytes <= self.capacity_bytes:
            raise ValueError(
                "free_bytes must be between zero and capacity_bytes"
            )

# Aggregate root
@dataclass(frozen=True)
class MountPointSnapshot:
    mount_point: MountPointMetrics

    def __repr__(self) -> str:
        return f"Mount point: {self.mount_point.mount_point} Bytes: {self.mount_point.capacity_bytes} Free: {self.mount_point.free_bytes} Usage: {self.mount_point.usage_percent:.2f}% Health: {self.overall_health()}"

    # business rule
    def overall_health(self) -> HealthStatus:
        if self.mount_point.usage_percent >= DISK_PERCENT_CRITICAL_THRESHOLD:
            return HealthStatus.CRITICAL

        if self.mount_point.usage_percent >= DISK_PERCENT_WARNING_THRESHOLD:
            return HealthStatus.WARNING

        return HealthStatus.OK