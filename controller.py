import consts

from typing import Optional

from console import Console
from hospital import Hospital


class InterfaceController:
    PATIENT_STATUS = 1
    USERS_COUNT = 200

    def __init__(self,):
        self.hospital = Hospital()
        self.init_patients()
        self.console = Console()
        
    def init_patients(self,):
        for i in range(self.USERS_COUNT):
            self.hospital.add_patient(self.PATIENT_STATUS)

    def _get_user_input(self, text: str = "Введите команду: ") -> str:
        return self.console.get_input(text)
    
    def _get_patient_id(self) -> Optional[int]:
        patient_id_raw = self._get_user_input("Введите ID пациента: ")
        try:
            return int(patient_id_raw)
        except Exception:
            self.console.put_output("Ошибка ввода. ID пациента должно быть числом (целым, положительным)")
    
    def _exec_patient_command(self, command):
        patient_id = self._get_patient_id()
        if patient_id is None:
            return
        if command in consts.DECREASE_PATIENT_STAT_CMDS:
            self.hospital.decrease_patient_status(patient_id)
            self.console.put_output(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
        elif command in consts.INCREASE_PATIENT_STAT_CMDS:
            self.hospital.increase_patient_status(patient_id)
            self.console.put_output(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
        else:
            self.console.put_output(f"Статус пациента: {self.hospital.get_patient_status_name(patient_id)}")

    def exec_command(self):
        command = self._get_user_input()
        if command in consts.STAT_CMDS:
            self.print_statistics()
        elif command in consts.STOP_CMDS:
            self.console.put_output("Сеанс завершён.")
            exit(0)
        elif command in consts.PATIENT_CMDS:
            self._exec_patient_command(command)
        else:
            self.console.put_output("Неизвестная команда! Попробуйте ещё раз.")

    def exec_command_v2(self):
        command = self._get_user_input()
        if command in consts.STAT_CMDS:
            self.print_statistics()
        elif command in consts.STOP_CMDS:
            self.console.put_output("Сеанс завершён.")
            exit()
        elif command in consts.DECREASE_PATIENT_STAT_CMDS:
            patient_id = self._get_patient_id()
            self.hospital.decrease_patient_status(patient_id)
            self.console.put_output(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
        elif command in consts.INCREASE_PATIENT_STAT_CMDS:
            patient_id = self._get_patient_id()
            self.hospital.increase_patient_status(patient_id)
            self.console.put_output(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
        elif command in consts.GET_PATIENT_STAT_CMDS:
            patient_id = self._get_patient_id()
            self.hospital.increase_patient_status(patient_id)
            self.console.put_output(f"Новый статус пациента: {self.hospital.get_patient_status_name(patient_id)}")
        else:
            self.console.put_output("Неизвестная команда! Попробуйте ещё раз.")
            
    def print_statistics(self,):
        # не выводим статистику по статусам болезни, на которых нет пациентов
        stat_to_print = list(
            filter(lambda stat: stat.patients_count > 0, self.hospital.get_statistics())
        )
        for stat in stat_to_print:
            self.console.put_output(f'- в статусе "{stat.status_name}": {stat.patients_count} чел.')
