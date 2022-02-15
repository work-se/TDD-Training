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


@pytest.mark.parametrize(
    "command", ("status down", "понизить статус пациента")
)
def test_decrease_patient_status(command):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Новый статус пациента: Тяжело болен")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()

    patient = interface_controller._hospital._patients[1]
    assert patient.status == 0, "Неверный статус пациента после изменения"


@pytest.mark.parametrize(
    "command", ("status down", "понизить статус пациента")
)
def test_decrease_min_patient_status(command):
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=0)])
    interface_controller = InterfaceController(console=console_mock, hospital=hospital)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("status up", "повысить статус пациента")
)
def test_increase_patient_status(command):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Новый статус пациента: Слегка болен")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()

    patient = interface_controller._hospital._patients[1]
    assert patient.status == 2, "Неверный статус пациента после изменения"


@pytest.mark.parametrize(
    "command", ("status up", "повысить статус пациента")
)
def test_increase_max_patient_status(command):
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
    interface_controller = InterfaceController(console=console_mock, hospital=hospital)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "нет")
    console_mock.add_expected_print('Пациент остался в статусе "Готов к выписке"')

    console_mock.add_expected_input("Введите команду: ", "get id")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Статус пациента: Готов к выписке")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("status up", "повысить статус пациента")
)
def test_increase_max_patient_status_with_discharge(command):
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
    interface_controller = InterfaceController(console=console_mock, hospital=hospital)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "да")
    console_mock.add_expected_print("Пациент выписан из больницы")

    console_mock.add_expected_input("Введите команду: ", "get id")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()


@pytest.mark.parametrize(
    "command", ("get id", "узнать статус пациента")
)
def test_get_patient_status(command):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console=console_mock)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Статус пациента: Болен")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

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
    console_mock.add_expected_print(print_text="Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Болен": 2 чел.')
    console_mock.add_expected_print('- в статусе "Слегка болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Готов к выписке": 1 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

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
    console_mock.add_expected_print(print_text="Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Болен": 2 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    interface_controller.exec_command()
