import pytest

from console import Console
from tests.interface_controller_test import conftest


def test_get_user_input(monkeypatch, interface_controller, check_get_user_input):
    monkeypatch.setattr(Console, "get_input", conftest.mock_get_input)
    check_get_user_input(interface_controller)


def test_get_patient_by_correct_input(monkeypatch, interface_controller, check_get_patient_with_correct_id):
    monkeypatch.setattr(Console, "get_input", conftest.mock_wrong_patient_id_output_check)
    monkeypatch.setattr(Console, "get_input", conftest.mock_get_user_id_input)
    check_get_patient_with_correct_id(interface_controller)


@pytest.mark.parametrize(
    "patch_func", (conftest.mock_get_user_id_wrong_input_1, conftest.mock_get_user_id_wrong_input_2)
)
def test_get_patient_by_wrong_input(monkeypatch, interface_controller, check_get_patient_with_wrong_id, patch_func):
    monkeypatch.setattr(Console, "get_input", patch_func)
    monkeypatch.setattr(Console, "get_input", patch_func)
    check_get_patient_with_wrong_id(interface_controller)


@pytest.mark.parametrize(
    "patch_input_func", (conftest.mock_get_input_command_stop_ru, conftest.mock_get_input_command_stop_en)
)
def test_close_command(monkeypatch, interface_controller, check_stop_command_actions, patch_input_func):
    monkeypatch.setattr(Console, "get_input", patch_input_func)
    check_stop_command_actions(interface_controller)
