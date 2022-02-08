import pytest

from hospital import Hospital
from tests.hostpital_tests import test_consts


def test_hospital_creation(hospital: Hospital, base_check_hospital):
    base_check_hospital(hospital)


@pytest.mark.parametrize(
    "patients",
    (
        test_consts.PATIENTS_TUPLE_1, test_consts.PATIENTS_TUPLE_2,
        test_consts.PATIENTS_TUPLE_3, test_consts.PATIENTS_TUPLE_4
    )
)
def test_add_patient_to_hospital(
    get_hospital_with_patients, base_check_hospital, check_patients_in_hospital, patients
):
    hospital = get_hospital_with_patients(patients)
    base_check_hospital(hospital, expected_patients_number=len(patients))
    check_patients_in_hospital(hospital, patients)


@pytest.mark.parametrize(
    "patients",
    (
        test_consts.PATIENTS_TUPLE_1, test_consts.PATIENTS_TUPLE_2,
        test_consts.PATIENTS_TUPLE_3, test_consts.PATIENTS_TUPLE_4
    )
)
def test_statistics_info(
    get_hospital_with_patients, check_statistics, patients
):
    hospital = get_hospital_with_patients(patients)
    check_statistics(hospital, patients)

