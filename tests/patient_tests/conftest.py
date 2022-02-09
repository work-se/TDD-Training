from loguru import logger
from pytest import fixture

from patient import Patient
from tests.patient_tests import test_consts


@fixture
def patient(create_patient) -> Patient:
    return create_patient(test_consts.DEFAULT_PATIENT_ID, test_consts.DEFAULT_STATUS_ID)


@fixture
def patient_with_min_disease_status(create_patient) -> Patient:
    return create_patient(test_consts.DEFAULT_PATIENT_ID, test_consts.MIN_DISEASE_ID)


@fixture
def patient_with_max_disease_status(create_patient) -> Patient:
    return create_patient(test_consts.DEFAULT_PATIENT_ID, test_consts.MAX_DISEASE_ID)


@fixture
def create_patient():
    def wrapper(patient_id: int, disease_id: int) -> Patient:
        return Patient(patient_id=patient_id, status=disease_id)

    return wrapper


@fixture
def check_patient_attributes():

    def wrapper(
        patient: Patient,
        expected_patient_id: int = test_consts.DEFAULT_PATIENT_ID,
        expected_disease_id: int = test_consts.DEFAULT_STATUS_ID
    ):
        logger.debug("Проверка пользователя {}", patient)
        assert patient.patient_id == expected_patient_id, "Неверный id пациента"
        assert patient.status == expected_disease_id, "Неверный статус болезни у пациента"

    return wrapper


@fixture
def check_patient_status():

    def wrapper(patient: Patient, expected_disease_id: int = test_consts.DEFAULT_STATUS_ID):
        logger.debug("Проверка статуса пользователя {}", patient)
        status = patient.get_status()
        assert status == expected_disease_id, "Неверный статус болезни у пациента"

    return wrapper
