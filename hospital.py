from typing import Dict, List, Iterable

from dtos.statistics_dto import StatisticsDto
from patient import Patient


class PatientDoesNotExists(Exception):

    def __init__(self):
        super().__init__("Ошибка. В больнице нет пациента с таким ID")


class PatientAlreadyWithMaxStatus(Exception):

    def __init__(self):
        super().__init__("Пациент уже с максимальным статусом")


class PatientAlreadyWithMinStatus(Exception):

    def __init__(self):
        super().__init__("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")


class Hospital:
    PATIENT_STATUSES = {
        0: "Тяжело болен",
        1: "Болен",
        2: "Слегка болен",
        3: "Готов к выписке"
    }
    MIN_STATUS = min(PATIENT_STATUSES.keys())
    MAX_STATUS = max(PATIENT_STATUSES.keys())
    
    def __init__(self, patients: Iterable[Patient] = None):
        self._patients: Dict[int, Patient] = {} if patients is None else self._form_patients_dict(patients)
        self._patients_index = len(self._patients)

    @staticmethod
    def _form_patients_dict(patients: Iterable[Patient]):
        return {
            patient.patient_id: patient
            for patient in patients
        }
    
    def add_patient(self, status: int) -> Patient:
        self._patients_index += 1
        new_patient = Patient(self._patients_index, status)
        self._patients[self._patients_index] = new_patient
        return new_patient

    def _get_patient(self, patient_id: int) -> Patient:
        patient = self._patients.get(patient_id)
        if patient is None:
            raise PatientDoesNotExists()
        return patient

    def discharge_patient(self, patient_id: int):
        self._get_patient(patient_id)
        del self._patients[patient_id]

    def can_increase_patient_status(self, patient_id: int) -> bool:
        patient = self._get_patient(patient_id)
        return patient.status != self.MAX_STATUS

    def increase_patient_status(self, patient_id: int):
        patient = self._get_patient(patient_id)
        if patient.status == self.MAX_STATUS:
            raise PatientAlreadyWithMaxStatus
        patient.increase_status()

    def can_decrease_patient_status(self, patient_id: int) -> bool:
        patient = self._get_patient(patient_id)
        return patient.status != self.MIN_STATUS

    def decrease_patient_status(self, patient_id: int):
        patient = self._get_patient(patient_id)
        if patient.status == self.MIN_STATUS:
            raise PatientAlreadyWithMinStatus
        patient.decrease_status()

    def get_patient_status_name(self, patient_id: int) -> str:
        patient = self._get_patient(patient_id)
        status = patient.get_status()
        return self.PATIENT_STATUSES[status]
    
    def get_statistics(self,) -> List[StatisticsDto]:
        return [
            StatisticsDto(
                status_name=status_name,
                patients_count=len(
                    list(
                        filter(lambda patient: patient.get_status() == status, self._patients.values())
                    )
                )
            )
            for status, status_name in self.PATIENT_STATUSES.items()
        ]

    def __repr__(self):
        return f"[Hospital] (patients num={self._patients_index}, patients={self._patients})"

    def __str__(self):
        return f"[Hospital] (patients num={self._patients_index}, patients={self._patients})"
