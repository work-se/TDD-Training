import consts

from typing import Optional

from console import Console, AbstractConsole
from hospital import Hospital, PatientDoesNotExists, PatientAlreadyWithMinStatus, PatientAlreadyWithMaxStatus


def catch_patient_does_not_exists(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except PatientDoesNotExists as exception:
            self._console.print(str(exception))

    return wrapper


class InterfaceController:
    PATIENT_STATUS = 1
    USERS_COUNT = 200

    def __init__(self, console: AbstractConsole = None, hospital: Hospital = None):
        self._hospital = self._get_hospital() if hospital is None else hospital
        self._console = Console() if console is None else console
        
    def _get_hospital(self):
        hospital = Hospital()
        for i in range(self.USERS_COUNT):
            hospital.add_patient(self.PATIENT_STATUS)
        return hospital
    
    def _get_patient_id(self) -> Optional[int]:
        patient_id_raw = self._console.input("Введите ID пациента: ")
        try:
            return int(patient_id_raw)
        except ValueError:
            self._console.print("Ошибка ввода. ID пациента должно быть числом (целым, положительным)")

    @catch_patient_does_not_exists
    def _decrease_patient_status(self, patient_id: int):
        try:
            self._hospital.decrease_patient_status(patient_id=patient_id)
            self._console.print(f"Новый статус пациента: {self._hospital.get_patient_status_name(patient_id)}")
        except PatientAlreadyWithMinStatus:
            self._console.print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    def _discharge_patient(self, patient_id: int):
        discharge_patient_answer = self._console.input("Желаете этого пациента выписать? (да/нет)")
        if discharge_patient_answer == "да":
            self._hospital.discharge_patient(patient_id)
            self._console.print("Пациент выписан из больницы")
            return

        status = self._hospital.get_patient_status_name(patient_id)
        self._console.print(f'Пациент остался в статусе "{status}"')

    @catch_patient_does_not_exists
    def _increase_patient_status(self, patient_id: int):
        try:
            self._hospital.increase_patient_status(patient_id)
            self._console.print(f"Новый статус пациента: {self._hospital.get_patient_status_name(patient_id)}")
        except PatientAlreadyWithMaxStatus:
            self._discharge_patient(patient_id)

    @catch_patient_does_not_exists
    def _get_patient_status(self, patient_id: int):
        status = self._hospital.get_patient_status_name(patient_id)
        self._console.print(f"Статус пациента: {status}")
    
    def _exec_patient_command(self, command):
        patient_id = self._get_patient_id()
        if patient_id is None:
            return
        if command in consts.DECREASE_PATIENT_STAT_CMDS:
            self._decrease_patient_status(patient_id)
        elif command in consts.INCREASE_PATIENT_STAT_CMDS:
            self._increase_patient_status(patient_id)
        else:
            self._get_patient_status(patient_id)

    def exec_command(self):
        while True:
            command = self._console.input("Введите команду: ")
            if command in consts.STAT_CMDS:
                self.print_statistics()
            elif command in consts.STOP_CMDS:
                self._console.print("Сеанс завершён.")
                break
            elif command in consts.PATIENT_CMDS:
                self._exec_patient_command(command)
            else:
                self._console.print("Неизвестная команда! Попробуйте ещё раз.")
            
    def print_statistics(self,):
        # не выводим статистику по статусам болезни, на которых нет пациентов
        stat_to_print = list(
            filter(lambda stat: stat.patients_count > 0, self._hospital.get_statistics())
        )
        self._console.print("Статистика по статусам:")
        for stat in stat_to_print:
            self._console.print(f'- в статусе "{stat.status_name}": {stat.patients_count} чел.')
