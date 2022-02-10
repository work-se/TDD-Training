from typing import Dict, List, Iterable

from dtos.statistics_dto import StatisticsDto
from patient import Patient


class Hospital:
    PATIENT_STATUSES = {
        0: "Тяжело болен",
        1: "Болен",
        2: "Слегка болен",
        3: "Готов к выписке"
    }
    
    def __init__(self, patients: Iterable[Patient] = None):
        self.patients: Dict[int, Patient] = {} if patients is None else self.form_patients_dict(patients)
        self.patients_number = len(self.patients)

    @staticmethod
    def form_patients_dict(patients: Iterable[Patient]):
        return {
            patient.patient_id: patient
            for patient in patients
        }
    
    def add_patient(self, status: int) -> Patient:
        self.patients_number += 1
        new_patient = Patient(self.patients_number, status)
        self.patients[self.patients_number] = new_patient
        return new_patient

    def increase_patient_status(self, patient_id: int):
        self.patients[patient_id].increase_status()

    def decrease_patient_status(self, patient_id: int):
        self.patients[patient_id].decrease_status()

    def get_patient_status_name(self, patient_id: int) -> str:
        status = self.patients[patient_id].get_status()
        return self.PATIENT_STATUSES[status]
    
    def get_statistics(self,) -> List[StatisticsDto]:
        return [
            StatisticsDto(
                status_name=status_name,
                patients_count=len(
                    list(
                        filter(lambda patient: patient.get_status() == status, self.patients.values())
                    )
                )
            )
            for status, status_name in self.PATIENT_STATUSES.items()
        ]

    def __repr__(self):
        return f"[Hospital] (patients num={self.patients_number}, patients={self.patients})"

    def __str__(self):
        return f"[Hospital] (patients num={self.patients_number}, patients={self.patients})"
