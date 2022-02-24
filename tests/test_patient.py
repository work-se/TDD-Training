from patient import Patient

# full unit-tests


def test_patient_create():
    patient = Patient(patient_id=1, status=2)
    assert patient.patient_id == 1, "Неверный id пациента"
    assert patient.status == 2, "Неверный статус болезни у пациента"


def test_increase_status():
    patient = Patient(patient_id=1, status=0)
    patient.increase_status()
    assert patient.status == 0 + 1, "Неверный статус болезни у пациента"


def test_decrease_status():
    patient = Patient(patient_id=1, status=2)
    patient.decrease_status()
    assert patient.status == 2 - 1, "Неверный статус болезни у пациента"


def test_get_status():
    patient = Patient(patient_id=1, status=2)
    status = patient.get_status()
    assert status == 2, "Неверный статус болезни у пациента"
