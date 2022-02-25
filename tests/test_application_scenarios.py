import pytest

from application import Application
from communications_controller import CommunicationsController
from hospital import Hospital
from hospital_controller import HospitalController
from patient import Patient
from tests.mocks.console_mock import ConsoleMock


def test_wrong_data_input():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="Неизвестная команда")
    console_mock.add_expected_print(print_text="Неизвестная команда! Попробуйте ещё раз.")

    for wrong_input_patient_id in ("asd", "1.2", "1,2"):
        console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="get id")
        console_mock.add_expected_input("Введите ID пациента: ", wrong_input_patient_id)
        console_mock.add_expected_print(
            print_text="Ошибка ввода. ID пациента должно быть числом (целым, положительным)"
        )

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()


@pytest.mark.parametrize(
    "command", ("status down", "status up", "get id")
)
def test_access_non_existent_patient(command):
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller, hospital)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)
    console_mock.add_expected_input("Введите ID пациента: ", "2")
    console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()


def test_decrease_patient_status_and_try_to_decrease_min_patient_status():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    init_test_hospital = Hospital(
        [Patient(1, 2), Patient(2, 2), Patient(3, 0)]
    )
    hospital_controller = HospitalController(communications_controller, init_test_hospital)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="status down")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Новый статус пациента: Болен")

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="status down")
    console_mock.add_expected_input("Введите ID пациента: ", "3")
    console_mock.add_expected_print(print_text="Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()

    end_test_hospital = Hospital(
        [Patient(1, 1), Patient(2, 2), Patient(3, 0)]
    )
    assert init_test_hospital == end_test_hospital, "Изменения в hospital после теста не соответствуют ожидаемым"


def test_increase_patient_status_and_discharge_patient():
    console_mock = ConsoleMock()
    init_test_hospital = Hospital(
        [Patient(1, 1), Patient(2, 3), Patient(3, 3)]
    )
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller, init_test_hospital)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="status up")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Новый статус пациента: Слегка болен")

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="status up")
    console_mock.add_expected_input("Введите ID пациента: ", "3")
    console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "нет")
    console_mock.add_expected_print('Пациент остался в статусе "Готов к выписке"')

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="status up")
    console_mock.add_expected_input("Введите ID пациента: ", "2")
    console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "да")
    console_mock.add_expected_print(print_text="Пациент выписан из больницы")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()

    end_test_hospital_patients = [
        Patient(1, 2), Patient(3, 3)
    ]
    assert init_test_hospital == end_test_hospital_patients, \
        "Изменения в hospital после теста не соответствуют ожидаемым"


def test_get_patient_status_and_hospital_statistics():
    console_mock = ConsoleMock()
    hospital = Hospital(
        [Patient(1, 1), Patient(2, 2), Patient(3, 2), Patient(4, 3)]
    )
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller, hospital)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="get id")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Статус пациента: Болен")

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="calculate statistics")
    console_mock.add_expected_print(print_text="Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Слегка болен": 2 чел.')
    console_mock.add_expected_print('- в статусе "Готов к выписке": 1 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()
