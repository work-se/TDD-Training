from unittest.mock import MagicMock

from hospital_controller import HospitalController
from tests.mocks.hospital_controller_mock import get_mocked_hospital_controller


def test_mocked_hospital_controller():
    hospital_controller = get_mocked_hospital_controller()
    assert isinstance(hospital_controller, HospitalController), "Возвраще неверный тип объекта"

    assert isinstance(hospital_controller.decrease_patient_status, MagicMock), \
        "Метод decrease_patient_status не замокан"
    assert isinstance(hospital_controller.increase_patient_status, MagicMock), \
        "Метод increase_patient_status не замокан"
    assert isinstance(hospital_controller.get_patient_status, MagicMock), "Метод get_patient_status не замокан"
    assert isinstance(hospital_controller.print_statistics, MagicMock), "Метод print_statistics не замокан"
