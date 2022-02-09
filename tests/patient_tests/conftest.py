from loguru import logger
from pytest import fixture

from patient import Patient
from tests.patient_tests import test_consts


@fixture
def patient(create_patient) -> Patient:
    return create_patient(test_consts.DEFAULT_PATIENT_ID, test_consts.DEFAULT_STATUS)


@fixture
def patient_with_min_status(create_patient) -> Patient:
    return create_patient(test_consts.DEFAULT_PATIENT_ID, test_consts.MIN_STATUS)


@fixture
def patient_with_max_status(create_patient) -> Patient:
    return create_patient(test_consts.DEFAULT_PATIENT_ID, test_consts.MAX_STATUS)


@fixture
def create_patient():
    def wrapper(patient_id: int, status: int) -> Patient:
        return Patient(patient_id=patient_id, status=status)

    return wrapper


@fixture
def check_patient_attributes():

    def wrapper(
        patient: Patient,
        expected_patient_id: int = test_consts.DEFAULT_PATIENT_ID,
        expected_status: int = test_consts.DEFAULT_STATUS
    ):
        logger.debug("Проверка пользователя {}", patient)
        assert patient.patient_id == expected_patient_id, "Неверный id пациента"
        assert patient.status == expected_status, "Неверный статус болезни у пациента"

    return wrapper


@fixture
def check_patient_status():

    def wrapper(patient: Patient, expected_status: int = test_consts.DEFAULT_STATUS):
        logger.debug("Проверка статуса пользователя {}", patient)
        status = patient.get_status()
        assert status == expected_status, "Неверный статус болезни у пациента"

    return wrapper
