import consts

from patient import Patient


def test_patient_create(patient: Patient, check_patient_attributes):
    check_patient_attributes(patient)


def test_increase_disease_status(patient_with_min_disease_status: Patient, check_patient_attributes):
    patient = patient_with_min_disease_status
    disease_ids_sorted = sorted(consts.PATIENT_STATUSES.keys())
    for expected_disease_id in disease_ids_sorted[1:]:
        patient.increase_disease_status()
        check_patient_attributes(patient=patient, expected_disease_id=expected_disease_id)


def test_decrease_disease_status(patient_with_max_disease_status: Patient, check_patient_attributes):
    patient = patient_with_max_disease_status
    disease_ids_sorted = sorted(consts.PATIENT_STATUSES.keys(), reverse=True)
    for expected_disease_id in disease_ids_sorted[1:]:
        patient.decrease_disease_status()
        check_patient_attributes(patient=patient, expected_disease_id=expected_disease_id)


def test_get_disease_status(patient_with_min_disease_status: Patient, check_patient_status):
    patient = patient_with_min_disease_status
    disease_ids_sorted = sorted(consts.PATIENT_STATUSES.keys())
    check_patient_status(patient, disease_ids_sorted[0])
    for disease_id in disease_ids_sorted[1:]:
        patient.increase_disease_status()
        check_patient_status(patient, disease_id)
