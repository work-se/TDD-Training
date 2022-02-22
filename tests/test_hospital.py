import pytest

from hospital import Hospital, PatientDoesNotExists, PatientAlreadyWithMaxStatus, PatientAlreadyWithMinStatus
from patient import Patient


def test_default_hospital_creation():
    hospital = Hospital()
    assert hospital._patients_index == 200, "Неверное количество пациентов"
    assert len(hospital._patients) == 200, "Количество объектов пациентов не совпадает со счетчиком пациентов"
    patients_statuses = list(set([patient.status for patient in hospital._patients.values()]))
    assert len(patients_statuses) == 1, "Пациенты созданы не с одинаковым статусом"
    assert patients_statuses[0] == 1, "Неверный статус у созданных пациентов"


def test_custom_hospital_creation():
    hospital = Hospital([Patient(patient_id=1, status=2)])
    assert hospital._patients_index == 1, "Неверное количество пациентов"
    assert len(hospital._patients) == 1, "Количество объектов пациентов не совпадает со счетчиком пациентов"
    assert hospital._patients.get(1) is not None, "Переданный пациент не сохранен в больнице"
    assert hospital._patients[1].status == 2, "Неверный статус у созданного пациента"


def test_add_patients_to_hospital():
    statuses = [0, 1, 2, 3, 0, 1]
    hospital = Hospital([])

    for status in statuses:
        hospital.add_patient(status=status)

    assert hospital._patients_index == len(statuses), "Неверное значение счетчика пациентов после создания"
    assert len(hospital._patients) == len(statuses), "Неверное количество пациентов после создания"

    patients = sorted(hospital._patients.values(), key=lambda item: item.patient_id)
    for patient, status in zip(patients, statuses):
        assert patient.status == status, "Неверный статус у созданного пользователя"


@pytest.fixture
def hospital_with_patient() -> Hospital:
    return Hospital(patients=[Patient(patient_id=1, status=1)])


def test_increase_patient_status(hospital_with_patient):
    hospital_with_patient.increase_patient_status(patient_id=1)
    assert hospital_with_patient._patients[1].status == 2, "Неверный статус у пациента после увеличения"


def test_increase_non_existent_patient_status():
    hospital = Hospital([])
    with pytest.raises(PatientDoesNotExists):
        hospital.increase_patient_status(patient_id=1)


def test_increase_minimum_status():
    hospital = Hospital(patients=[Patient(patient_id=1, status=3)])

    with pytest.raises(PatientAlreadyWithMaxStatus) as exception:
        hospital.increase_patient_status(patient_id=1)
    assert "Пациент уже с максимальным статусом" in str(exception.value)


def test_decrease_patient_status(hospital_with_patient):
    hospital_with_patient.decrease_patient_status(patient_id=1)
    assert hospital_with_patient._patients[1].status == 0, "Неверный статус у пациента после уменьшения"


def test_decrease_non_existent_patient_status():
    hospital = Hospital([])
    with pytest.raises(PatientDoesNotExists):
        hospital.decrease_patient_status(patient_id=1)


def test_decrease_minimum_status():
    hospital = Hospital(patients=[Patient(patient_id=1, status=0)])

    with pytest.raises(PatientAlreadyWithMinStatus) as exception:
        hospital.decrease_patient_status(patient_id=1)
    assert "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)" == str(exception.value)


def test_get_patient_status(hospital_with_patient):
    status_name = hospital_with_patient.get_patient_status_name(patient_id=1)
    assert status_name == "Болен", "Неверный статус у пациента после увеличения"


def test_get_non_existent_patient_status():
    hospital = Hospital([])
    with pytest.raises(PatientDoesNotExists):
        hospital.get_patient_status_name(patient_id=1)


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


def test_get_patient():
    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])

    try:
        patient = hospital._get_patient(1)
    except PatientDoesNotExists:
        assert False, "Ложное срабатывание проверки на существующего пользователя"

    assert patient.patient_id == 1, "Получен неверный пользователь по id"


def test_check_patient_does_not_exists():
    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])

    with pytest.raises(PatientDoesNotExists) as exception:
        hospital._get_patient(2)
    assert "Ошибка. В больнице нет пациента с таким ID" == str(exception.value), "Неожиданный вывод в ошибке"


def test_discharge_patient():
    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
    hospital.discharge_patient(1)

    assert hospital._patients.get(1) is None, "После выписки пациент остался в больнице"


def test_discharge_non_existed_patient():
    hospital = Hospital([])
    with pytest.raises(PatientDoesNotExists):
        hospital.discharge_patient(1)


def test_can_increase_patient_status():
    hospital = Hospital(patients=[Patient(patient_id=1, status=3)])
    assert hospital.can_increase_patient_status(1) is False, \
        "Неверный результат проверки увеличения максимального статуса"

    hospital = Hospital(patients=[Patient(patient_id=1, status=2)])
    assert hospital.can_increase_patient_status(1) is True, \
        "Неверный результат проверки увеличения НЕ максимального статуса"


def test_can_decrease_patient_status():
    hospital = Hospital(patients=[Patient(patient_id=1, status=0)])
    assert hospital.can_decrease_patient_status(1) is False, \
        "Неверный результат проверки уменьшения минимального статуса"

    hospital = Hospital(patients=[Patient(patient_id=1, status=1)])
    assert hospital.can_decrease_patient_status(1) is True, \
        "Неверный результат проверки уменьшения НЕ минимального статуса"

