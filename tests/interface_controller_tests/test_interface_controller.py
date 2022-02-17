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


def test_get_patient_id():
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console_mock)

    console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
    patient_id = interface_controller._get_patient_id()
    assert patient_id == 1, "Получен неверный id пациента"


@pytest.mark.parametrize(
    "wrong_id", ("asd", "1.2", "1,2")
)
def test_get_patient_with_wrong_id(wrong_id):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console_mock)

    console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input=wrong_id)
    console_mock.add_expected_print(print_text="Ошибка ввода. ID пациента должно быть числом (целым, положительным)")
    patient_id = interface_controller._get_patient_id()
    assert patient_id is None, "Получен какой-то id пациента при неверном вводе"


def test_decrease_patient_status():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
    interface_controller = InterfaceController(console_mock, hospital)
    console_mock.add_expected_print(print_text='Новый статус пациента: Тяжело болен')

    interface_controller._decrease_patient_status(1)
    patient = interface_controller._hospital._patients[1]
    assert patient.status == 0, "Неверный статус пациента после понижения"


def test_decrease_min_patient_status():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=0)])
    interface_controller = InterfaceController(console_mock, hospital)

    console_mock.add_expected_print(print_text="Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
    interface_controller._decrease_patient_status(1)
    patient = interface_controller._hospital._patients[1]
    assert patient.status == 0, "Неверный статус пациента после понижения минимального статуса"


def test_successful_discharge_patient():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
    interface_controller = InterfaceController(console_mock, hospital)
    console_mock.add_expected_input(expected_text="Желаете этого пациента выписать? (да/нет)", expected_input="да")
    console_mock.add_expected_print(print_text="Пациент выписан из больницы")

    interface_controller._discharge_patient(1)
    patient = interface_controller._hospital._patients.get(1)
    assert patient is None, "После выписки пациент остался в больнице"


def test_unsuccessful_discharge_patient():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
    interface_controller = InterfaceController(console_mock, hospital)
    console_mock.add_expected_input(expected_text="Желаете этого пациента выписать? (да/нет)", expected_input="нет")
    console_mock.add_expected_print(print_text='Пациент остался в статусе "Готов к выписке"')

    interface_controller._discharge_patient(1)
    patient = interface_controller._hospital._patients.get(1)
    assert patient is not None, "После НЕ выписки пациент, его нет в больнице"


def test_increase_patient_status():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
    interface_controller = InterfaceController(console_mock, hospital)
    console_mock.add_expected_print(print_text='Новый статус пациента: Слегка болен')

    interface_controller._increase_patient_status(1)
    patient = interface_controller._hospital._patients[1]
    assert patient.status == 2, "Неверный статус пациента после повышения"


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


class MockMethodCalled(Exception):
    """
    Проверка вызова замоканого метода
    """
    pass


def test_increase_max_patient_status():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
    interface_controller = InterfaceController(console_mock, hospital)

    def _discharge_patient(patient_id):
        assert patient_id == 1, "Неверный id передан для выписывания пациента"
        raise MockMethodCalled

    interface_controller._discharge_patient = _discharge_patient

    with pytest.raises(MockMethodCalled):
        interface_controller._increase_patient_status(1)


def test_get_patient_status():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
    interface_controller = InterfaceController(console_mock, hospital)
    console_mock.add_expected_print(print_text="Статус пациента: Болен")

    interface_controller._get_patient_status(1)


def test_non_existent_patient_decrease_status():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[])
    interface_controller = InterfaceController(console_mock, hospital)
    console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

    interface_controller._decrease_patient_status(1)


def test_non_existent_patient_increase_status():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[])
    interface_controller = InterfaceController(console_mock, hospital)
    console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

    interface_controller._increase_patient_status(1)


def test_non_existent_patient_get_status():
    console_mock = ConsoleMock()
    hospital = Hospital(patients=[])
    interface_controller = InterfaceController(console_mock, hospital)
    console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

    interface_controller._get_patient_status(1)


@pytest.fixture
def hospital_with_all_status_patients() -> Hospital:
    hospital = Hospital()
    hospital.add_patient(0)
    hospital.add_patient(1)
    hospital.add_patient(1)
    hospital.add_patient(2)
    hospital.add_patient(3)
    return hospital


def test_get_all_statuses_statistics(hospital_with_all_status_patients):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console_mock, hospital_with_all_status_patients)

    console_mock.add_expected_print(print_text="Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Болен": 2 чел.')
    console_mock.add_expected_print('- в статусе "Слегка болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Готов к выписке": 1 чел.')

    interface_controller.print_statistics()


@pytest.fixture
def hospital_with_limit_status_patients() -> Hospital:
    hospital = Hospital()
    hospital.add_patient(0)
    hospital.add_patient(1)
    hospital.add_patient(1)
    return hospital


def test_get_limit_statuses_statistics( hospital_with_limit_status_patients):
    console_mock = ConsoleMock()
    interface_controller = InterfaceController(console_mock, hospital_with_limit_status_patients)

    console_mock.add_expected_print(print_text="Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Болен": 2 чел.')

    interface_controller.print_statistics()

