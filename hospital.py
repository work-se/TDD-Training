from typing import Optional, List

import consts
from dtos.statistics_dto import StatisticsDto
from patient import Patient


class Hospital:
    
    def __init__(self,):
        self.patients = {}
        self.patients_number = 0
        
    @classmethod
    def get_disease_id(cls, disease_name: Optional[str]) -> int:
        return consts.DEFAULT_DISEASE_ID or consts.DISEASE_STATUSES_REVERSED[disease_name]
    
    def add_patient(self, disease_name: str = None) -> Patient:
        disease_id = self.get_disease_id(disease_name)
        self.patients_number += 1
        new_patient = Patient(self.patients_number, disease_id)
        self.patients[self.patients_number] = new_patient
        return new_patient
    
    def get_statistics(self,) -> List[StatisticsDto]:
        return [
            StatisticsDto(
                disease=disease_name,
                patients_count=len(
                    list(filter(lambda patient: patient.status == disease_id, self.patients.values()))
                )
            )
            for disease_id, disease_name in consts.DISEASE_STATUSES.items()
        ]
        
            
        
