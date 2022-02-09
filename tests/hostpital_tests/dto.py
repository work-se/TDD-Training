from dataclasses import dataclass


@dataclass(frozen=True)
class ExpectedPatientsCompoundDto:
    patient_id: int
    status: int

    def __str__(self):
        return f"[Patient] (id={self.patient_id}, status={self.status})"
