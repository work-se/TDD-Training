import consts

from typing import Optional

from console import Console, AbstractConsole
from hospital import Hospital


class InterfaceController:
    PATIENT_STATUS = 1
    USERS_COUNT = 200

    def __init__(self, console: AbstractConsole = None, hospital: Hospital = None):
        self.hospital = self.get_hospital() if hospital is None else hospital
        self.console = Console() if console is None else console
        
    def get_hospital(self):
        hospital = Hospital()
        for i in range(self.USERS_COUNT):
            hospital.add_patient(self.PATIENT_STATUS)
        return hospital

    def _get_user_input(self, text: str = "Введите команду: ") -> str:
        return self.console.input(text)
    
    def _get_patient_id(self) -> Optional[int]:
        patient_id_raw = self._get_user_input("Введите ID пациента: ")
        try:
            return int(patient_id_raw)
        except ValueError:
            self.console.print("Ошибка ввода. ID пациента должно быть числом (целым, положительным)")
    
    def _exec_patient_command(self, command):
        patient_id = self._get_patient_id()
        if patient_id is None:
            return
        if command in consts.DECREASE_PATIENT_STAT_CMDS:
            self.hospital.decrease_patient_status(patient_id)
            self.console.print(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
        elif command in consts.INCREASE_PATIENT_STAT_CMDS:
            self.hospital.increase_patient_status(patient_id)
            self.console.print(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
        else:
            self.console.print(f"Статус пациента: {self.hospital.get_patient_status_name(patient_id)}")

    def exec_command(self):
        while True:
            command = self._get_user_input()
            if command in consts.STAT_CMDS:
                self.print_statistics()
            elif command in consts.STOP_CMDS:
                self.console.print("Сеанс завершён.")
                break
            elif command in consts.PATIENT_CMDS:
                self._exec_patient_command(command)
            else:
                self.console.print("Неизвестная команда! Попробуйте ещё раз.")

    def exec_command_v2(self):
        while True:
            command = self._get_user_input()
            if command in consts.STAT_CMDS:
                self.print_statistics()
            elif command in consts.STOP_CMDS:
                self.console.print("Сеанс завершён.")
                break
            elif command in consts.DECREASE_PATIENT_STAT_CMDS:
                patient_id = self._get_patient_id()
                self.hospital.decrease_patient_status(patient_id)
                self.console.print(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
            elif command in consts.INCREASE_PATIENT_STAT_CMDS:
                patient_id = self._get_patient_id()
                self.hospital.increase_patient_status(patient_id)
                self.console.print(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
            elif command in consts.GET_PATIENT_STAT_CMDS:
                patient_id = self._get_patient_id()
                self.hospital.increase_patient_status(patient_id)
                self.console.print(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
            else:
                self.console.print("Неизвестная команда! Попробуйте ещё раз.")
            
    def print_statistics(self,):
        # не выводим статистику по статусам болезни, на которых нет пациентов
        stat_to_print = list(
            filter(lambda stat: stat.patients_count > 0, self.hospital.get_statistics())
        )
        self.console.print("Статистика по статусам:")
        for stat in stat_to_print:
            self.console.print(f'- в статусе "{stat.status_name}": {stat.patients_count} чел.')
