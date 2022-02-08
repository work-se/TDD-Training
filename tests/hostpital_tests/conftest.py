import consts

from pytest import fixture
from loguru import logger
from typing import List, Dict

from hospital import Hospital
from tests.hostpital_tests.dto import ExpectedPatientsCompoundDto


@fixture
def hospital() -> Hospital:
    return Hospital()


@fixture
def get_hospital_with_patients():

    def wrapper(patients: List[ExpectedPatientsCompoundDto]) -> Hospital:
        hospital = Hospital()
        for patient in patients:
            hospital.add_patient(disease_name=consts.DISEASE_STATUSES[patient.disease_id])
        return hospital

    return wrapper


@fixture
def base_check_hospital():

    def wrapper(
        hospital: Hospital, expected_patients_number: int = 0
    ):
        assert hospital.patients_number == expected_patients_number, "Неверное количество пациентов"
        assert len(hospital.patients) == expected_patients_number, \
            "Количество объектов пациентов не совпадает со счетчиком пациентов"

    return wrapper


@fixture
def check_patients_in_hospital():

    def wrapper(hospital: Hospital, expected_patients: List[ExpectedPatientsCompoundDto]):
        logger.debug(f"Ожидаемые пациенты: {expected_patients}")
        logger.debug(f"Больница: {hospital}")
        for expected_patient in expected_patients:
            assert expected_patient.patient_id in hospital.patients, \
                f"В больнице нет ожидаемого пациента с id {expected_patient.patient_id}"
            patient = hospital.patients[expected_patient.patient_id]
            assert patient.patient_id == expected_patient.patient_id, \
                f"В больнице под id {expected_patient.patient_id}, находится другой пациент с id {patient.patient_id}"
            assert patient.status == expected_patient.disease_id, "Пациент имеет неверный статус болезни"

    return wrapper


@fixture
def check_statistics():

    def form_patients_disease_dict(expected_patients: List[ExpectedPatientsCompoundDto]) -> Dict[str, int]:
        data_dict = {}
        for patient in expected_patients:
            disease_name = consts.DISEASE_STATUSES[patient.disease_id]
            disease = data_dict.get(disease_name)
            if disease is None:
                data_dict[disease_name] = 1
                continue
            data_dict[disease_name] += 1
        return data_dict

    def wrapper(hospital: Hospital, expected_patients: List[ExpectedPatientsCompoundDto]):
        logger.debug(f"Больница: {hospital}")
        expected_data_dict = form_patients_disease_dict(expected_patients)
        logger.debug(f"Ожидаемая статистика: {expected_data_dict}")
        statistics = hospital.get_statistics()
        assert set([statistic.disease for statistic in statistics]) == set(consts.DISEASE_STATUSES.values()), \
            "В статистике отражены не все статусы болезней"

        for statistic_element in statistics:
            assert expected_data_dict.get(statistic_element.disease, 0) == statistic_element.patients_count, \
                f"Неверное количество пациентов в статистике для болезни {statistic_element.disease}"

    return wrapper
