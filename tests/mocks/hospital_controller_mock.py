from hospital_controller import HospitalController
from unittest.mock import MagicMock


def get_mocked_hospital_controller():
    hospital_controller = HospitalController()
    hospital_controller.decrease_patient_status = MagicMock()
    hospital_controller.increase_patient_status = MagicMock()
    hospital_controller.get_patient_status = MagicMock()
    hospital_controller.print_statistics = MagicMock()

    return hospital_controller
