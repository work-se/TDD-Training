import consts

from dtos.patient_dto import PatienStatDto


class Patient:
    
    def __init__(self, patient_id: int, status: int):
        self.patient_id = patient_id
        self.status = status
        
    def increase_disease_status(self,):
        self.status += 1
        
    def decrease_disease_status(self,):
        self.status -= 1
    
    def get_disease_status(self,) -> PatienStatDto:
        return PatienStatDto(
            disease_id=self.status, disease_name=consts.DISEASE_STATUSES[self.status]
        )
    
    
    
        
