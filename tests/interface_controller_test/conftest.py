from pytest import fixture, raises

from controller import InterfaceController
from hospital import Hospital


@fixture
def interface_controller() -> InterfaceController:
    return InterfaceController()


def check_execution_of_stop_command(interface_controller: InterfaceController):
    with raises(SystemExit) as exit_data:
        interface_controller.exec_command()
    assert exit_data.type == SystemExit
    assert exit_data.value.code == 0


def patch_patients_in_hospital(hospital: Hospital):
    hospital.increase_patient_status(1)
    hospital.increase_patient_status(1)
    hospital.increase_patient_status(2)
    hospital.decrease_patient_status(3)

