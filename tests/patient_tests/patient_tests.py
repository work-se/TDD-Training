from patient import Patient


def test_patient_create():
    patient = Patient(patient_id=1, status=2)
    assert patient.patient_id == 1, "Неверный id пациента"
    assert patient.status == 2, "Неверный статус болезни у пациента"


def test_increase_status():
    status = 0
    patient = Patient(patient_id=1, status=status)
    patient.increase_status()
    assert patient.status == status + 1, "Неверный статус болезни у пациента"


def test_decrease_status():
    status = 2
    patient = Patient(patient_id=1, status=status)
    patient.decrease_status()
    assert patient.status == status - 1, "Неверный статус болезни у пациента"


def test_get_status():
    expected_status = 2
    patient = Patient(patient_id=1, status=expected_status)
    status = patient.get_status()
    assert status == expected_status, "Неверный статус болезни у пациента"
