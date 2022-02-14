import pytest

from controller import InterfaceController
from hospital import Hospital
from patient import Patient
from tests.console_mock import ConsoleMock


def test_wrong_command_input():
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="Неизвестная команда")
    console_mock.add_expected_print(print_text="Неизвестная команда! Попробуйте ещё раз.")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("stop", "стоп")
)
def test_stop_command(command):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_print(print_text="Сеанс завершён.")
    interface_controller.exec_command()


@pytest.mark.parametrize(
    "wrong_id", ("asd", "1.2", "1,2")
)
def test_input_wrong_patient_id(wrong_id):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="get id")
    console_mock.add_expected_input("Введите ID пациента: ", wrong_id)
    console_mock.add_expected_print(print_text="Ошибка ввода. ID пациента должно быть числом (целым, положительным)")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("status down", "status up", "get id")
)
def test_access_non_existent_patient(command):
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
    interface_controller = InterfaceController(console=console_mock, hospital=hospital)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "2")
    console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()