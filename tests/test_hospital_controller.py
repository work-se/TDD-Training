import pytest

from unittest.mock import MagicMock

from hospital import Hospital
from hospital_controller import HospitalController
from patient import Patient
from tests.console_mock import ConsoleMock


def test_decrease_patient_status():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
        console_mock.add_expected_print(print_text='Новый статус пациента: Тяжело болен')

        hospital_controller.decrease_patient_status()
        patient = hospital_controller._hospital._patients[1]
        assert patient.status == 0, "Неверный статус пациента после понижения"


def test_decrease_min_patient_status():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[Patient(patient_id=1, status=0)])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
        console_mock.add_expected_print(
            print_text="Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)"
        )

        hospital_controller.decrease_patient_status()
        patient = hospital_controller._hospital._patients[1]
        assert patient.status == 0, "Неверный статус пациента после понижения минимального статуса"


def test_successful_discharge_patient():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Желаете этого пациента выписать? (да/нет)", expected_input="да")
        console_mock.add_expected_print(print_text="Пациент выписан из больницы")

        hospital_controller._discharge_patient(1)
        patient = hospital_controller._hospital._patients.get(1)
        assert patient is None, "После выписки пациент остался в больнице"


def test_unsuccessful_discharge_patient():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Желаете этого пациента выписать? (да/нет)", expected_input="нет")
        console_mock.add_expected_print(print_text='Пациент остался в статусе "Готов к выписке"')

        hospital_controller._discharge_patient(1)
        patient = hospital_controller._hospital._patients.get(1)
        assert patient is not None, "После НЕ выписки пациент, его нет в больнице"


def test_increase_patient_status():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
        console_mock.add_expected_print(print_text='Новый статус пациента: Слегка болен')

        hospital_controller.increase_patient_status()
        patient = hospital_controller._hospital._patients[1]
        assert patient.status == 2, "Неверный статус пациента после повышения"


def test_increase_max_patient_status():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
        hospital_controller._discharge_patient = MagicMock()

        hospital_controller.increase_patient_status()
        hospital_controller._discharge_patient.assert_called()


def test_get_patient_status():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
        console_mock.add_expected_print(print_text="Статус пациента: Болен")

        hospital_controller.get_patient_status()


def test_non_existent_patient_decrease_status():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
        console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

        hospital_controller.decrease_patient_status()


def test_non_existent_patient_increase_status():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
        console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

        hospital_controller.increase_patient_status()


def test_non_existent_patient_get_status():
    with ConsoleMock() as console_mock:
        hospital = Hospital(patients=[])
        hospital_controller = HospitalController(console_mock, hospital)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")
        console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

        hospital_controller.get_patient_status()


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
    with ConsoleMock() as console_mock:
        hospital_controller = HospitalController(console_mock, hospital_with_all_status_patients)

        console_mock.add_expected_print(print_text="Статистика по статусам:")
        console_mock.add_expected_print('- в статусе "Тяжело болен": 1 чел.')
        console_mock.add_expected_print('- в статусе "Болен": 2 чел.')
        console_mock.add_expected_print('- в статусе "Слегка болен": 1 чел.')
        console_mock.add_expected_print('- в статусе "Готов к выписке": 1 чел.')

        hospital_controller.print_statistics()


@pytest.fixture
def hospital_with_limit_status_patients() -> Hospital:
    hospital = Hospital()
    hospital.add_patient(0)
    hospital.add_patient(1)
    hospital.add_patient(1)
    return hospital


def test_get_limit_statuses_statistics(hospital_with_limit_status_patients):
    with ConsoleMock() as console_mock:
        hospital_controller = HospitalController(console_mock, hospital_with_limit_status_patients)

        console_mock.add_expected_print(print_text="Статистика по статусам:")
        console_mock.add_expected_print('- в статусе "Тяжело болен": 1 чел.')
        console_mock.add_expected_print('- в статусе "Болен": 2 чел.')

        hospital_controller.print_statistics()
