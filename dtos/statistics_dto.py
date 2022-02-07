from dataclasses import dataclass


@dataclass(frozen=True)
class StatisticsDto:
    disease: str
    patients_count: int
