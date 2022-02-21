from unittest.mock import MagicMock

import pytest

from controller import InterfaceController
from tests.console_mock import ConsoleMock


def test_get_hospital():
    interface_controller = InterfaceController()

    hospital = interface_controller._get_hospital()
    assert len(hospital._patients) == 200, "Неверное количество пациентов создано"
    for patient in hospital._patients.values():
        assert patient.status == 1, "Неверный статус у созданных пациентов"


def test_correct_english_commands_mapping():
    with ConsoleMock() as console_mock:
        interface_controller = InterfaceController(console_mock)
        hospital_controller = interface_controller._hospital_controller

        console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="calculate statistics")
        console_mock.add_expected_input("Введите команду: ", "status down")
        console_mock.add_expected_input("Введите команду: ", "status up")
        console_mock.add_expected_input("Введите команду: ", "get id")
        console_mock.add_expected_input("Введите команду: ", "stop")

        hospital_controller.decrease_patient_status = MagicMock()
        hospital_controller.increase_patient_status = MagicMock()
        hospital_controller.get_patient_status = MagicMock()
        hospital_controller.print_statistics = MagicMock()
        interface_controller._communication_controller.print_end_session = MagicMock()

        interface_controller.exec_command()
        hospital_controller.print_statistics.assert_called()
        hospital_controller.decrease_patient_status.assert_called()
        hospital_controller.increase_patient_status.assert_called()
        hospital_controller.get_patient_status.assert_called()
        interface_controller._communication_controller.print_end_session.assert_called()


def test_correct_russian_commands_mapping():
    with ConsoleMock() as console_mock:
        interface_controller = InterfaceController(console_mock)
        hospital_controller = interface_controller._hospital_controller

        console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="рассчитать статистику")
        console_mock.add_expected_input("Введите команду: ", "понизить статус пациента")
        console_mock.add_expected_input("Введите команду: ", "повысить статус пациента")
        console_mock.add_expected_input("Введите команду: ", "узнать статус пациента")
        console_mock.add_expected_input("Введите команду: ", "стоп")

        hospital_controller.decrease_patient_status = MagicMock()
        hospital_controller.increase_patient_status = MagicMock()
        hospital_controller.get_patient_status = MagicMock()
        hospital_controller.print_statistics = MagicMock()
        interface_controller._communication_controller.print_end_session = MagicMock()

        interface_controller.exec_command()
        hospital_controller.print_statistics.assert_called()
        hospital_controller.decrease_patient_status.assert_called()
        hospital_controller.increase_patient_status.assert_called()
        hospital_controller.get_patient_status.assert_called()
        interface_controller._communication_controller.print_end_session.assert_called()
