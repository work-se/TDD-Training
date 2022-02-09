from dataclasses import dataclass


@dataclass(frozen=True)
class StatisticsDto:
    status_name: str
    patients_count: int
