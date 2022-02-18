from unittest.mock import MagicMock

import pytest

from controller import InterfaceController
from hospital import Hospital
from patient import Patient
from tests.console_mock import ConsoleMock


def test_get_hospital():
    interface_controller = InterfaceController()

    hospital = interface_controller._get_hospital()
    assert len(hospital._patients) == 200, "Неверное количество пациентов создано"
    for patient in hospital._patients.values():
        assert patient.status == 1, "Неверный статус у созданных пациентов"

# todo: add tests on exec_func with hospital controller calls mock


# def test_status_down():
#     cmd = make_commands()
#     cmd._dialog_with_user.request_patient_id = MagicMock(return_value=77)
#     cmd._hospital.patient_status_down = MagicMock()
#     cmd._hospital.get_patient_status_by_id = MagicMock(return_value='Слегка болен')
#     cmd._dialog_with_user.send_message = MagicMock()
#
#     cmd.status_down()
#
#     cmd._dialog_with_user.request_patient_id.assert_called_with()
#     cmd._hospital.patient_status_down.assert_called_with(77)
#     cmd._hospital.get_patient_status_by_id.assert_called_with(77)
#     cmd._dialog_with_user.send_message.assert_called_with('Новый статус пациента: "Слегка болен"')
#
#
# def test_status_down_when_patient_id_not_integer():
#     cmd = make_commands()
#     cmd._dialog_with_user.request_patient_id = MagicMock(side_effect=PatientIdNotIntegerError)
#     cmd._dialog_with_user.send_message = MagicMock()
#
#     cmd.status_down()
#
#     cmd._dialog_with_user.request_patient_id.assert_called_with()
#     cmd._dialog_with_user.send_message.assert_called_with('Ошибка ввода. '
#                                                           'ID пациента должно быть числом (целым, положительным)')




