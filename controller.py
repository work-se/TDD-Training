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
    
    def _exec_patient_command(self, command):
        patient = self._get_patient()
        if patient is None:
            return
        if command in consts.DECREASE_PATIENT_STAT_CMDS:
            patient.decrease_disease_status()
            print(f"Новый статус пациента: {patient.get_disease_status().disease_name}")
        if command in consts.INCREASE_PATIENT_STAT_CMDS:
            patient.increase_disease_status()
            print(f"Новый статус пациента: {patient.get_disease_status().disease_name}")
        elif command in consts.GET_PATIENT_STAT_CMDS:
            print(f"Статус пациента: {patient.get_disease_status().disease_name}")

    def exec_command(self):
        command = self._get_user_input()
        if command in consts.STAT_CMDS:
            self.print_statistics()
        elif command in consts.STOP_CMDS:
            print("Сеанс завершён.")
            exit()
        elif command in consts.PATIENT_CMDS:
            self._exec_patient_command(command)
        else:
            print("Неизвестная команда! Попробуйте ещё раз.")

    def exec_command_v2(self):
        command = self._get_user_input()
        if command in consts.STAT_CMDS:
            self.print_statistics()
        elif command in consts.STOP_CMDS:
            print("Сеанс завершён.")
            exit()
        elif command in consts.DECREASE_PATIENT_STAT_CMDS:
            patient = self._get_patient()
            patient.decrease_disease_status()
            print(f"Новый статус пациента: {patient.get_disease_status().disease_name}")
        elif command in consts.INCREASE_PATIENT_STAT_CMDS:
            patient = self._get_patient()
            patient.increase_disease_status()
            print(f"Новый статус пациента: {patient.get_disease_status().disease_name}")
        elif command in consts.GET_PATIENT_STAT_CMDS:
            patient = self._get_patient()
            print(f"Статус пациента: {patient.get_disease_status().disease_name}")
        else:
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
