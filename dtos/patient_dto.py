from dataclasses import dataclass


@dataclass(frozen=True)
class PatienStatDto:
    disease_id: int
    disease_name: str
