import pytest

from unittest.mock import MagicMock

from application import Application
from communications_controller import CommunicationsController, CommandTypes
from hospital import Hospital
from hospital_controller import HospitalController
from patient import Patient
from tests.mocks.console_mock import ConsoleMock
from tests.mocks.hospital_controller_mock import get_mocked_hospital_controller


# Application в данном случае является менеджером, который по вводу определяет требующийся порядок вызовов,
# поэтому будем реализовывать как Unit-test + mock


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


def test_correct_commands_mapping():

    hospital_controller = get_mocked_hospital_controller()
    communication_controller = CommunicationsController()
    application = Application(communication_controller, hospital_controller)
    communication_controller.print_end_session = MagicMock()

    application.exec_command(CommandTypes.GET_PATIENT_STAT)
    hospital_controller.get_patient_status.assert_called()

    application.exec_command(CommandTypes.INCREASE_PATIENT_STAT)
    hospital_controller.increase_patient_status.assert_called()

    application.exec_command(CommandTypes.DECREASE_PATIENT_STAT)
    hospital_controller.decrease_patient_status.assert_called()

    application.exec_command(CommandTypes.CALCULATE_STAT)
    hospital_controller.print_statistics.assert_called()

    application.exec_command(CommandTypes.STOP)
    communication_controller.print_end_session.assert_called()


def test_check_continue_loop():
    for command in CommandTypes:
        continue_loop_result = Application._check_continue_loop(command)
        if command != CommandTypes.STOP:
            assert continue_loop_result is True, "Неверное значение для продолжения цикла выполнения команд"
        else:
            assert continue_loop_result is False, "Неверное значение остановки цикла при команде стоп"
