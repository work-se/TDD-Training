import pytest

from hospital import Hospital
from patient import Patient


def test_hospital_creation():
    hospital = Hospital()
    assert hospital.patients_number == 0, "Неверное количество пациентов"
    assert len(hospital.patients) == 0, "Количество объектов пациентов не совпадает со счетчиком пациентов"


def test_add_patients_to_hospital():
    statuses = [0, 1, 2, 3, 0, 1]
    hospital = Hospital()

    for status in statuses:
        hospital.add_patient(status=status)

    assert hospital.patients_number == len(statuses), "Неверное значение счетчика пациентов после создания"
    assert len(hospital.patients) == len(statuses), "Неверное количество пациентов после создания"

    patients = sorted(hospital.patients.values(), key=lambda item: item.patient_id)
    for patient, status in zip(patients, statuses):
        assert patient.status == status, "Неверный статус у созданного пользователя"


@pytest.mark.parametrize(
    "patients,expected_statistics",
    [
        # несколько пациентов с одним статусом
        (
            (Patient(patient_id=1, status=1), Patient(patient_id=2, status=1)),
            {"Тяжело болен": 0, "Болен": 2, "Слегка болен": 0, "Готов к выписке": 0}
        ),
        # несколько пациентов с различными статусами (половина статусов)
        (
            (Patient(patient_id=1, status=1), Patient(patient_id=2, status=2)),
            {"Тяжело болен": 0, "Болен": 1, "Слегка болен": 1, "Готов к выписке": 0}
        ),
        # несколько пациентов с различными статусами и статусы повторяются
        (
            (
                Patient(patient_id=1, status=0), Patient(patient_id=2, status=3),
                Patient(patient_id=3, status=0), Patient(patient_id=4, status=3)
            ),
            {"Тяжело болен": 2, "Болен": 0, "Слегка болен": 0, "Готов к выписке": 2}
        ),
        # пациенты со всеми возможными статусами болезней
        (
            (
                Patient(patient_id=1, status=0), Patient(patient_id=2, status=0),
                Patient(patient_id=3, status=1), Patient(patient_id=4, status=2),
                Patient(patient_id=5, status=3)
            ),
            {"Тяжело болен": 2, "Болен": 1, "Слегка болен": 1, "Готов к выписке": 1}
        ),
    ]
)
def test_statistics_info(patients, expected_statistics):
    hospital = Hospital(patients)
    statistics = hospital.get_statistics()
    assert set([statistic.status_name for statistic in statistics]) == set(expected_statistics.keys()), \
        "В статистике отражены не все статусы болезней"

    for statistic_element in statistics:
        assert expected_statistics[statistic_element.status_name] == statistic_element.patients_count, \
            f"Неверное количество пациентов в статистике для болезни {statistic_element.status_name}"
