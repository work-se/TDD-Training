from typing import Optional

import consts
from hospital import Hospital
from patient import Patient


class InterfaceController:

    def __init__(self,):
        self.hospital = Hospital()
        self.init_patients()
        
    def init_patients(self,):
        for i in range(200):
            self.hospital.add_patient()
            
    @classmethod
    def _get_user_input(cls, text: str = "Введите команду: ") -> str:
        return input(text)
    
    def _get_patient(self) -> Optional[Patient]:
        patient_id_raw = self._get_user_input("Введите ID пациента: ")
        try:
            patient_id = int(patient_id_raw)
            return self.hospital.patients[patient_id]
        except Exception:
            print("Ошибка ввода. ID пациента должно быть числом (целым, положительным)")
    
    def _patient_cmd(self, command):
        patient = self._get_patient()
        if patient is None:
            return
        
        match command:
            case consts.DECREASE_PATIENT_STAT_CMD_RU | consts.DECREASE_PATIENT_STAT_CMD_EN:
                patient.decrease_disease_status()
                print(f"Новый статус пациента: {patient.get_disease_status().disease_name}")
            case consts.INCREASE_PATIENT_STAT_CMD_RU | consts.INCREASE_PATIENT_STAT_CMD_EN:
                patient.increase_disease_status()
                print(f"Новый статус пациента: {patient.get_disease_status().disease_name}")
            case consts.GET_PATIENT_STAT_CMD_RU | consts.GET_PATIENT_STAT_CMD_EN:
                print(f"Статус пациента: {patient.get_disease_status().disease_name}")
        
            
    def exec_command(self):
        command = self._get_user_input()
        match command:
            case consts.STAT_CMD_RU | consts.STAT_CMD_EN:
                self.print_statistics()
            case consts.STOP_CMD_RU | consts.STOP_CMD_EN:
                print("Сеанс завершён.")
                exit()
            case consts.DECREASE_PATIENT_STAT_CMD_RU | consts.DECREASE_PATIENT_STAT_CMD_EN | \
                consts.INCREASE_PATIENT_STAT_CMD_RU | consts.INCREASE_PATIENT_STAT_CMD_EN | \
                consts.GET_PATIENT_STAT_CMD_RU | consts.GET_PATIENT_STAT_CMD_EN:
                self._patient_cmd(command)
            case _:
                print("Неизвестная команда! Попробуйте ещё раз.")
            
    def print_statistics(self,):
        # не выводим статистику по статусам болезни, на которых нет пациентов
        stat_to_print = list(
            filter(lambda stat: stat.patients_count > 0, self.hospital.get_statistics())
        )
        if not stat_to_print:
            print("Всем похорошело, пациентов нет!")
            return
        for stat in stat_to_print:
            print(f'- в статусе "{stat.disease}": {stat.patients_count} чел.')
