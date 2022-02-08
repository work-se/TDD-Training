from dataclasses import dataclass


@dataclass(frozen=True)
class ExpectedPatientsCompoundDto:
    patient_id: int
    disease_id: int

    def __str__(self):
        return f"[Patient] (id={self.patient_id}, status={self.disease_id})"
