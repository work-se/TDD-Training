from enum import Enum
from typing import Optional, Iterable

from console import Console
from dtos.statistics_dto import StatisticsDto


class ReceivedInvalidId(Exception):

    def __init__(self):
        super().__init__("Ошибка ввода. ID пациента должно быть числом (целым, положительным)")


class CommandTypes(Enum):

    def __new__(cls, value_en: str, value_ru: str):
        obj = object.__new__(cls)
        obj._value_ = value_en
        obj._value_ru = value_ru
        cls._value2member_map_[value_en] = obj
        cls._value2member_map_[value_ru] = obj

        return obj

    STOP = "stop", "стоп"
    CALCULATE_STAT = "calculate statistics", "рассчитать статистику"
    DECREASE_PATIENT_STAT = "status down", "понизить статус пациента"
    INCREASE_PATIENT_STAT = "status up", "повысить статус пациента"
    GET_PATIENT_STAT = "get id", "узнать статус пациента"


class CommunicationsController:

    def __init__(self, console=None):
        self._console = console if console is not None else Console()

    def print_change_patient_status(self, status: str):
        self._console.print(f"Новый статус пациента: {status}")

    def print_current_patient_status(self, status: str):
        self._console.print(f"Статус пациента: {status}")

    def print_patient_status_not_changed(self, status: str):
        self._console.print(f'Пациент остался в статусе "{status}"')

    def print_end_session(self):
        self._console.print("Сеанс завершён.")

    def print_hospital_statistics(self, statuses_info: Iterable[StatisticsDto]):
        self._console.print("Статистика по статусам:")
        for status_info in statuses_info:
            self._console.print(f'- в статусе "{status_info.status_name}": {status_info.patients_count} чел.')

    def print_patients_cant_die(self):
        self._console.print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    def print_patient_discharged(self):
        self._console.print("Пациент выписан из больницы")

    def print_exception(self, exception: str):
        self._console.print(exception)

    def get_command(self) -> Optional[CommandTypes]:
        command = self._console.input("Введите команду: ")
        parsed_command = None
        try:
            parsed_command = CommandTypes(command.lower())
        except ValueError:
            self._console.print("Неизвестная команда! Попробуйте ещё раз.")
        return parsed_command

    def get_patient_id(self) -> Optional[int]:
        patient_id_raw = self._console.input("Введите ID пациента: ")
        try:
            return int(patient_id_raw)
        except ValueError:
            raise ReceivedInvalidId

    def request_confirm_discharge_patient(self) -> bool:
        answer = self._console.input("Желаете этого пациента выписать? (да/нет)")
        return "да" == answer
