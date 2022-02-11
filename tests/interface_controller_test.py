import pytest

from controller import InterfaceController
from hospital import Hospital
from tests.console_mock import ConsoleMock


@pytest.mark.parametrize(
    "command", ("status down", "понизить статус пациента")
)
def test_decrease_patient_status(command):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_output(output="Новый статус пациента: Тяжело болен")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_output("Сеанс завершён.")

    interface_controller.exec_command()

    patient = interface_controller._hospital._patients[1]
    assert patient.status == 0, "Неверный статус пациента после изменения"


@pytest.mark.parametrize(
    "command", ("status up", "повысить статус пациента")
)
def test_increase_patient_status(command):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_output(output="Новый статус пациента: Слегка болен")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_output("Сеанс завершён.")

    interface_controller.exec_command()

    patient = interface_controller._hospital._patients[1]
    assert patient.status == 2, "Неверный статус пациента после изменения"


def test_wrong_command_input():
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="Неизвестная команда")
    console_mock.add_expected_output(output="Неизвестная команда! Попробуйте ещё раз.")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_output("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("stop", "стоп")
)
def test_stop_command(command):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_output(output="Сеанс завершён.")
    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("get id", "узнать статус пациента")
)
def test_get_patient_status(command):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_output(output="Статус пациента: Болен")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_output("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "wrong_id", ("asd", "1.2", "1,2")
)
def test_input_wrong_patient_id(wrong_id):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="get id")
    console_mock.add_expected_input("Введите ID пациента: ", wrong_id)
    console_mock.add_expected_output(output="Ошибка ввода. ID пациента должно быть числом (целым, положительным)")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_output("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.fixture
def hospital_with_all_status_patients() -> Hospital:
    hospital = Hospital()
    hospital.add_patient(0)
    hospital.add_patient(1)
    hospital.add_patient(1)
    hospital.add_patient(2)
    hospital.add_patient(3)
    return hospital


@pytest.mark.parametrize(
    "command", ("рассчитать статистику", "calculate statistics")
)
def test_get_all_statuses_statistics(command, hospital_with_all_status_patients):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock, hospital=hospital_with_all_status_patients)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_output(output="Статистика по статусам:")
    console_mock.add_expected_output('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_output('- в статусе "Болен": 2 чел.')
    console_mock.add_expected_output('- в статусе "Слегка болен": 1 чел.')
    console_mock.add_expected_output('- в статусе "Готов к выписке": 1 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_output("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.fixture
def hospital_with_limit_status_patients() -> Hospital:
    hospital = Hospital()
    hospital.add_patient(0)
    hospital.add_patient(1)
    hospital.add_patient(1)
    return hospital


@pytest.mark.parametrize(
    "command", ("рассчитать статистику", "calculate statistics")
)
def test_get_limit_statuses_statistics(command, hospital_with_limit_status_patients):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock, hospital=hospital_with_limit_status_patients)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_output(output="Статистика по статусам:")
    console_mock.add_expected_output('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_output('- в статусе "Болен": 2 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_output("Сеанс завершён.")

    interface_controller.exec_command()


def test_complex_script_1():
    """
    Тестовый сценарий № 1 (стандартный)
    сценарий из файла tasks/Тренинг_по_архитектуре_итерация_1.md
    """
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="узнать статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_output(output="Статус пациента: Болен")

    console_mock.add_expected_input("Введите команду: ", "повысить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "2")
    console_mock.add_expected_output("Новый статус пациента: Слегка болен")

    console_mock.add_expected_input("Введите команду: ", "понизить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "3")
    console_mock.add_expected_output("Новый статус пациента: Тяжело болен")

    console_mock.add_expected_input("Введите команду: ", "рассчитать статистику")
    console_mock.add_expected_output("Статистика по статусам:")
    console_mock.add_expected_output('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_output('- в статусе "Болен": 198 чел.')
    console_mock.add_expected_output('- в статусе "Слегка болен": 1 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_output("Сеанс завершён.")

    interface_controller.exec_command()
