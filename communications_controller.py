from enum import Enum
from typing import Optional

from console import Console


class CommandTypes(Enum):

    def __new__(cls, value_en: str, value_ru: str):
        print("HEre")
        print(f"{value_en} - {value_ru}")
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

    def print_end_session(self):
        self._console.print("Сеанс завершён.")

    def get_command(self) -> Optional[CommandTypes]:
        command = self._console.input("Введите команду: ")
        try:
            return CommandTypes(command)
        except ValueError:
            self._console.print("Неизвестная команда! Попробуйте ещё раз.")

    def get_patient_id(self) -> Optional[int]:
        patient_id_raw = self._console.input("Введите ID пациента: ")
        try:
            return int(patient_id_raw)
        except ValueError:
            self._console.print("Ошибка ввода. ID пациента должно быть числом (целым, положительным)")

    def ask_confirm_discharge_patient(self) -> bool:
        answer = self._console.input("Желаете этого пациента выписать? (да/нет)")
        return "да" == answer
