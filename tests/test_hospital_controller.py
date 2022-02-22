from unittest.mock import MagicMock

from communications_controller import CommunicationsController
from hospital import Hospital, PatientAlreadyWithMinStatus, PatientDoesNotExists, StatisticsDto
from hospital_controller import HospitalController
from patient import Patient
from tests.console_mock import ConsoleMock


def test_default_hospital_controller_creations():
    hospital_controller = HospitalController()
    assert isinstance(hospital_controller._hospital, Hospital), "Неверный тип атрибута объекта после создания"
    assert isinstance(hospital_controller._communication_controller, CommunicationsController), \
        "Неверный тип атрибута объекта после создания"


def test_custom_hospital_controller_creations():
    hospital = Hospital(patients=[Patient(patient_id=1, status=2)])
    communications_controller = CommunicationsController(ConsoleMock())
    hospital_controller = HospitalController(communications_controller, hospital)

    assert hospital_controller._hospital._patients_index == 1, \
        "Сохраненный атрибут _hospital отличается от переданного в конструкторе"
    assert hospital_controller._hospital._patients.get(1) is not None, \
        "Сохраненный атрибут _hospital отличается от переданного в конструкторе"
    assert hospital_controller._hospital._patients[1] == Patient(patient_id=1, status=2), \
        "Сохраненный атрибут _hospital отличается от переданного в конструкторе"

    assert isinstance(communications_controller._console, ConsoleMock), \
        "Сохраненный атрибут _communications_controller отличается от переданного в конструкторе"


def test_decrease_patient_status():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.decrease_patient_status = MagicMock()
    hospital.get_patient_status_name = MagicMock(return_value="Новый статус пациента")
    communication_controller.print_change_patient_status = MagicMock()

    hospital_controller.decrease_patient_status()
    communication_controller.get_patient_id.assert_called()
    hospital.decrease_patient_status.assert_called_with(1)
    hospital.get_patient_status_name.assert_called_with(1)
    communication_controller.print_change_patient_status.assert_called_with("Новый статус пациента")


def test_decrease_min_patient_status():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.decrease_patient_status = MagicMock(side_effect=PatientAlreadyWithMinStatus)
    communication_controller.print_exception = MagicMock()

    hospital_controller.decrease_patient_status()
    communication_controller.get_patient_id.assert_called()
    hospital.decrease_patient_status.assert_called_with(1)
    communication_controller.print_exception.assert_called_with(
        "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)"
    )


def test_increase_patient_status():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.can_increase_patient_status = MagicMock(return_value=True)
    hospital.increase_patient_status = MagicMock()
    hospital.get_patient_status_name = MagicMock(return_value="Новый статус пациента")
    communication_controller.print_change_patient_status = MagicMock()

    hospital_controller.increase_patient_status()

    communication_controller.get_patient_id.assert_called()
    hospital.can_increase_patient_status.assert_called_with(1)
    hospital.increase_patient_status.assert_called_with(1)
    hospital.get_patient_status_name.assert_called_with(1)
    communication_controller.print_change_patient_status.assert_called_with("Новый статус пациента")


def test_increase_max_patient_status_and_discharge_patient():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.can_increase_patient_status = MagicMock(return_value=False)
    hospital.increase_patient_status = MagicMock()
    communication_controller.request_confirm_discharge_patient = MagicMock(return_value=True)
    hospital.discharge_patient = MagicMock()
    communication_controller.print_patient_discharged = MagicMock()

    hospital_controller.increase_patient_status()
    communication_controller.get_patient_id.assert_called()
    hospital.can_increase_patient_status.assert_called_with(1)
    hospital.increase_patient_status.assert_not_called()
    communication_controller.request_confirm_discharge_patient.assert_called()
    hospital.discharge_patient.assert_called_with(1)
    communication_controller.print_patient_discharged.assert_called()


def test_increase_max_patient_status_and_not_discharge_patient():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.can_increase_patient_status = MagicMock(return_value=False)
    hospital.increase_patient_status = MagicMock()
    communication_controller.request_confirm_discharge_patient = MagicMock(return_value=False)
    hospital.discharge_patient = MagicMock()
    hospital.get_patient_status_name = MagicMock(return_value="Текущий статус")
    communication_controller.print_patient_status_not_changed = MagicMock()

    hospital_controller.increase_patient_status()
    communication_controller.get_patient_id.assert_called()
    hospital.can_increase_patient_status.assert_called_with(1)
    hospital.increase_patient_status.assert_not_called()
    communication_controller.request_confirm_discharge_patient.assert_called()
    hospital.discharge_patient.assert_not_called()
    hospital.get_patient_status_name.assert_called()
    communication_controller.print_patient_status_not_changed.assert_called_with("Текущий статус")


def test_get_patient_status():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.get_patient_status_name = MagicMock(return_value="Текущий статус")
    communication_controller.print_current_patient_status = MagicMock()

    hospital_controller.get_patient_status()

    communication_controller.get_patient_id.assert_called()
    hospital.get_patient_status_name.assert_called_with(1)
    communication_controller.print_current_patient_status.assert_called_with("Текущий статус")


def test_non_existent_patient_decrease_status():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.decrease_patient_status = MagicMock(side_effect=PatientDoesNotExists)
    communication_controller.print_exception = MagicMock()

    hospital_controller.decrease_patient_status()
    communication_controller.get_patient_id.assert_called()
    hospital.decrease_patient_status.assert_called()
    communication_controller.print_exception.assert_called_with("Ошибка. В больнице нет пациента с таким ID")


def test_non_existent_patient_increase_status():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.can_increase_patient_status = MagicMock(side_effect=PatientDoesNotExists)
    hospital.increase_patient_status = MagicMock()
    communication_controller.print_exception = MagicMock()

    hospital_controller.increase_patient_status()
    communication_controller.get_patient_id.assert_called()
    hospital.can_increase_patient_status.assert_called()
    hospital.increase_patient_status.assert_not_called()
    communication_controller.print_exception.assert_called_with("Ошибка. В больнице нет пациента с таким ID")


def test_non_existent_patient_get_status():
    hospital_controller = HospitalController()
    hospital = hospital_controller._hospital
    communication_controller = hospital_controller._communication_controller

    communication_controller.get_patient_id = MagicMock(return_value=1)
    hospital.get_patient_status_name = MagicMock(side_effect=PatientDoesNotExists)
    communication_controller.print_exception = MagicMock()

    hospital_controller.get_patient_status()
    communication_controller.get_patient_id.assert_called()
    hospital.get_patient_status_name.assert_called()
    communication_controller.print_exception.assert_called_with("Ошибка. В больнице нет пациента с таким ID")


def test_print_all_received_from_hospital_statistics():
    hospital_controller = HospitalController()
    communication_controller = hospital_controller._communication_controller
    hospital = hospital_controller._hospital

    statistics = [
        StatisticsDto(status_name="Статус 1", patients_count=1),
        StatisticsDto(status_name="Статус 2", patients_count=2)
    ]
    hospital.get_statistics = MagicMock(return_value=statistics)
    communication_controller.print_hospital_statistics = MagicMock()

    hospital_controller.print_statistics()
    hospital.get_statistics.assert_called()
    communication_controller.print_hospital_statistics.assert_called_with(statistics)


def test_print_limit_received_from_hospital_statistics():
    hospital_controller = HospitalController()
    communication_controller = hospital_controller._communication_controller
    hospital = hospital_controller._hospital

    hospital.get_statistics = MagicMock(return_value=[
            StatisticsDto(status_name="Статус 1", patients_count=1),
            StatisticsDto(status_name="Статус 2", patients_count=0)
        ])
    communication_controller.print_hospital_statistics = MagicMock()

    hospital_controller.print_statistics()
    hospital.get_statistics.assert_called()
    communication_controller.print_hospital_statistics.assert_called_with(
        [StatisticsDto(status_name="Статус 1", patients_count=1)]
    )
