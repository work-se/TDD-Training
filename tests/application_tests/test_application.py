from unittest.mock import MagicMock

from application import Application
from communications_controller import CommunicationsController
from hospital import Hospital
from hospital_controller import HospitalController
from patient import Patient
from tests.console_mock import ConsoleMock


def test_default_application_creation():
    application = Application()
    assert isinstance(application._communications_controller, CommunicationsController), \
        "Неверный тип атрибута _communication_controller после инициализации объекта"
    assert isinstance(application._hospital_controller, HospitalController), \
        "Неверный тип атрибута _hospital_controller после инициализации объекта"


def test_custom_application_creation():
    communication_controller = CommunicationsController(ConsoleMock())
    hospital_controller = HospitalController(hospital=Hospital([Patient(patient_id=1, status=2)]))
    application = Application(communication_controller, hospital_controller)

    assert application._hospital_controller._hospital._patients_index == 1, \
        "Сохраненный атрибут _hospital отличается от переданного в конструкторе"
    assert application._hospital_controller._hospital._patients.get(1) is not None, \
        "Сохраненный атрибут _hospital отличается от переданного в конструкторе"
    assert application._hospital_controller._hospital._patients[1] == Patient(patient_id=1, status=2), \
        "Сохраненный атрибут _hospital отличается от переданного в конструкторе"

    assert isinstance(application._communications_controller._console, ConsoleMock), \
        "Сохраненный атрибут _communications_controller отличается от переданного в конструкторе"


def test_correct_english_commands_mapping():
    with ConsoleMock() as console_mock:
        application = Application(CommunicationsController(console_mock))
        hospital_controller = application._hospital_controller

        console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="calculate statistics")
        console_mock.add_expected_input("Введите команду: ", "status down")
        console_mock.add_expected_input("Введите команду: ", "status up")
        console_mock.add_expected_input("Введите команду: ", "get id")
        console_mock.add_expected_input("Введите команду: ", "stop")

        hospital_controller.decrease_patient_status = MagicMock()
        hospital_controller.increase_patient_status = MagicMock()
        hospital_controller.get_patient_status = MagicMock()
        hospital_controller.print_statistics = MagicMock()
        application._communications_controller.print_end_session = MagicMock()

        application.exec_command()
        hospital_controller.print_statistics.assert_called()
        hospital_controller.decrease_patient_status.assert_called()
        hospital_controller.increase_patient_status.assert_called()
        hospital_controller.get_patient_status.assert_called()
        application._communications_controller.print_end_session.assert_called()


def test_correct_russian_commands_mapping():
    with ConsoleMock() as console_mock:
        application = Application(CommunicationsController(console_mock))
        hospital_controller = application._hospital_controller

        console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="рассчитать статистику")
        console_mock.add_expected_input("Введите команду: ", "понизить статус пациента")
        console_mock.add_expected_input("Введите команду: ", "повысить статус пациента")
        console_mock.add_expected_input("Введите команду: ", "узнать статус пациента")
        console_mock.add_expected_input("Введите команду: ", "стоп")

        hospital_controller.decrease_patient_status = MagicMock()
        hospital_controller.increase_patient_status = MagicMock()
        hospital_controller.get_patient_status = MagicMock()
        hospital_controller.print_statistics = MagicMock()
        application._communications_controller.print_end_session = MagicMock()

        application.exec_command()
        hospital_controller.print_statistics.assert_called()
        hospital_controller.decrease_patient_status.assert_called()
        hospital_controller.increase_patient_status.assert_called()
        hospital_controller.get_patient_status.assert_called()
        application._communications_controller.print_end_session.assert_called()
