import pytest

from communications_controller import CommunicationsController, CommandTypes
from tests.console_mock import ConsoleMock


@pytest.mark.parametrize(
    "command,expected_command",
    (
        ("stop", CommandTypes.STOP), ("стоп", CommandTypes.STOP),
        ("calculate statistics", CommandTypes.CALCULATE_STAT), ("рассчитать статистику", CommandTypes.CALCULATE_STAT),
        ("status down", CommandTypes.DECREASE_PATIENT_STAT),
        ("понизить статус пациента", CommandTypes.DECREASE_PATIENT_STAT),
        ("status up", CommandTypes.INCREASE_PATIENT_STAT),
        ("повысить статус пациента", CommandTypes.INCREASE_PATIENT_STAT),
        ("get id", CommandTypes.GET_PATIENT_STAT), ("узнать статус пациента", CommandTypes.GET_PATIENT_STAT),
    )
)
def test_get_command(command, expected_command):
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)

    parsed_command = communications_controller.get_command()
    assert parsed_command == expected_command, "Текст преобразован в неверную команду"


def test_get_wrong_command():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input(expected_text="Введите команду", expected_input="wrong command")
    console_mock.add_expected_print(print_text="Неизвестная команда! Попробуйте ещё раз.")

    parsed_command = communications_controller.get_command()
    assert parsed_command is None, "Неизвестная команда преобразована в какую-то из известных команд"


def test_patient_id():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")

    patient_id = communications_controller.get_patient_id()
    assert patient_id == 1, "Получен неожиданный id пациента"


@pytest.mark.parametrize(
    "wrong_id", ("asd", "1.2", "1,2")
)
def test_wrong_patient_id(wrong_id):
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input=wrong_id)
    console_mock.add_expected_print(print_text="Ошибка ввода. ID пациента должно быть числом (целым, положительным)")

    patient_id = communications_controller.get_patient_id()
    assert patient_id is None, "Получен неожиданный id пациента"


def test_confirm_discharge_patient():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)

    console_mock.add_expected_input(expected_text="Желаете этого пациента выписать? (да/нет)", expected_input="да")
    answer = communications_controller.ask_confirm_discharge_patient()
    assert answer is True, "Неверно интерпретировано подтверждение выписки пациента"

    console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "нет")
    answer = communications_controller.ask_confirm_discharge_patient()
    assert answer is False, "Неверно интерпретировано подтверждение выписки пациента"


def test_print_change_patient_status():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(print_text="Новый статус пациента: Новый статус")

    communications_controller.print_change_patient_status("Новый статус")


def test_print_current_patient_status():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(print_text="Статус пациента: Текущий статус")

    communications_controller.print_current_patient_status("Текущий статус")


def test_print_end_session():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(print_text="Сеанс завершён.")

    communications_controller.print_end_session()
