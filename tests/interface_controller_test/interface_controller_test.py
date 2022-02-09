import pytest

from tests.interface_controller_test import conftest
from tests.interface_controller_test.mock.console_mock import ConsoleMock


@pytest.mark.parametrize(
    "command", ("status down", "понизить статус пациента")
)
def test_decrease_patient_status(monkeypatch, interface_controller, command):
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.mock_put_output()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    mocker.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
    mocker.add_expected_output(output="Новый статус пациента: Тяжело болен")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("status up", "повысить статус пациента")
)
def test_increase_patient_status(monkeypatch, interface_controller, command):
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.mock_put_output()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    mocker.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
    mocker.add_expected_output(output="Новый статус пациента: Слегка болен")

    interface_controller.exec_command()


def test_wrong_command_input(monkeypatch, interface_controller):
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.mock_put_output()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input="Неизвестная команда")
    mocker.add_expected_output(output="Неизвестная команда! Попробуйте ещё раз.")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("stop", "стоп")
)
def test_stop_command(monkeypatch, interface_controller, command):
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.add_expected_input(expected_text="Введите команду: ", expected_input=command)

    conftest.check_execution_of_stop_command(interface_controller)


@pytest.mark.parametrize(
    "command", ("stop", "стоп")
)
def test_stop_command(monkeypatch, interface_controller, command):
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.add_expected_input(expected_text="Введите команду: ", expected_input=command)

    conftest.check_execution_of_stop_command(interface_controller)


@pytest.mark.parametrize(
    "command", ("get id", "узнать статус пациента")
)
def test_get_patient_status(monkeypatch, interface_controller, command):
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.mock_put_output()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    mocker.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
    mocker.add_expected_output(output="Статус пациента: Болен")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "wrong_id", ("asd", "1.2", "1,2")
)
def test_input_wrong_patient_id(monkeypatch, interface_controller, wrong_id):
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.mock_put_output()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input="get id")
    mocker.add_expected_input(expected_text="Введите ID пациента: ", expected_input=wrong_id)
    mocker.add_expected_output(output="Ошибка ввода. ID пациента должно быть числом (целым, положительным)")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("рассчитать статистику", "calculate statistics")
)
def test_get_statistics(monkeypatch, interface_controller, command):
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.mock_put_output()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    mocker.add_expected_output(output="Статистика по статусам:")
    mocker.add_expected_output(output='- в статусе "Тяжело болен": 1 чел.')
    mocker.add_expected_output(output='- в статусе "Болен": 197 чел.')
    mocker.add_expected_output(output='- в статусе "Слегка болен": 1 чел.')
    mocker.add_expected_output(output='- в статусе "Готов к выписке": 1 чел.')

    conftest.patch_patients_in_hospital(interface_controller.hospital)
    interface_controller.exec_command()


def test_complex_script_1(monkeypatch, interface_controller):
    """
    Тестовый сценарий № 1 (стандартный)
    сценарий из файла tasks/Тренинг_по_архитектуре_итерация_1.md
    """
    mocker = ConsoleMock(monkeypatch)
    mocker.mock_get_input()
    mocker.mock_put_output()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input="узнать статус пациента")
    mocker.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
    mocker.add_expected_output(output="Статус пациента: Болен")
    interface_controller.exec_command()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input="повысить статус пациента")
    mocker.add_expected_input(expected_text="Введите ID пациента: ", expected_input="2")
    mocker.add_expected_output(output="Новый статус пациента: Слегка болен")
    interface_controller.exec_command()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input="понизить статус пациента")
    mocker.add_expected_input(expected_text="Введите ID пациента: ", expected_input="3")
    mocker.add_expected_output(output="Новый статус пациента: Тяжело болен")
    interface_controller.exec_command()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input="рассчитать статистику")
    mocker.add_expected_output(output="Статистика по статусам:")
    mocker.add_expected_output(output='- в статусе "Тяжело болен": 1 чел.')
    mocker.add_expected_output(output='- в статусе "Болен": 198 чел.')
    mocker.add_expected_output(output='- в статусе "Слегка болен": 1 чел.')
    interface_controller.exec_command()

    mocker.add_expected_input(expected_text="Введите команду: ", expected_input="stop")
    mocker.add_expected_output(output="Сеанс завершён.")
    conftest.check_execution_of_stop_command(interface_controller)
