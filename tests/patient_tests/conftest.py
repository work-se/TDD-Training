from loguru import logger

import consts
from tests.patient_tests import test_consts

from pytest import fixture

from patient import Patient
from dtos.patient_dto import PatienStatDto


@fixture
def patient(create_patient) -> Patient:
    return create_patient(test_consts.DEFAULT_PATIENT_ID, test_consts.DEFAULT_DISEASE_ID)


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
        expected_disease_id: int = test_consts.DEFAULT_DISEASE_ID
    ):
        logger.debug("Проверка пользователя {}", patient)
        assert patient.patient_id == expected_patient_id, "Неверный id пациента"
        assert patient.status == expected_disease_id, "Неверный статус болезни у пациента"

    return wrapper


@fixture
def check_patient_status():

    def wrapper(patient: Patient, expected_disease_id: int = test_consts.DEFAULT_DISEASE_ID):
        logger.debug("Проверка статуса пользователя {}", patient)
        status = patient.get_disease_status()
        assert type(status) == PatienStatDto, "Неожиданный тип статуса пациента"
        assert status.disease_id == expected_disease_id, "Неверный статус болезни у пациента"
        assert status.disease_name == consts.DISEASE_STATUSES[expected_disease_id], \
            "Неверное наименование статуса болезни пациента"

    return wrapper
