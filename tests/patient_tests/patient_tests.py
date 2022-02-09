from hospital import Hospital
from patient import Patient


def test_patient_create(patient: Patient, check_patient_attributes):
    check_patient_attributes(patient)


def test_increase_status(patient_with_min_status: Patient, check_patient_attributes):
    patient = patient_with_min_status
    statuses_sorted = sorted(Hospital.PATIENT_STATUSES.keys())
    for expected_status in statuses_sorted[1:]:
        patient.increase_status()
        check_patient_attributes(patient=patient, expected_status=expected_status)


def test_decrease_status(patient_with_max_status: Patient, check_patient_attributes):
    patient = patient_with_max_status
    statuses_sorted = sorted(Hospital.PATIENT_STATUSES.keys(), reverse=True)
    for expected_status in statuses_sorted[1:]:
        patient.decrease_status()
        check_patient_attributes(patient=patient, expected_status=expected_status)


def test_get_status(patient_with_min_status: Patient, check_patient_status):
    patient = patient_with_min_status
    statuses_sorted = sorted(Hospital.PATIENT_STATUSES.keys())
    check_patient_status(patient, statuses_sorted[0])
    for status in statuses_sorted[1:]:
        patient.increase_status()
        check_patient_status(patient, status)
