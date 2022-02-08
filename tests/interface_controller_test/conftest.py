import consts

from pytest import fixture, raises
from loguru import logger

from controller import InterfaceController
from tests.interface_controller_test import test_consts


@fixture
def interface_controller() -> InterfaceController:
    return InterfaceController()


@staticmethod
def mock_get_input(text: str):
    assert text == test_consts.DEFAULT_OUTPUT_STR, "Переда неверный текст для вывода в консоль пользователю"
    return test_consts.DEFAULT_INPUT_STR


@fixture
def check_get_user_input():

    def wrapper(interface_controller: InterfaceController):
        response = interface_controller._get_user_input(test_consts.DEFAULT_OUTPUT_STR)
        assert response == test_consts.DEFAULT_INPUT_STR

    return wrapper


@staticmethod
def mock_get_user_id_input(text: str):
    assert text == consts.INPUT_PATIENT_ID_COMMAND_TEXT, "Неверный текст для ввода id пациента"
    return test_consts.USER_ID_INPUT


@fixture
def check_get_patient_with_correct_id():

    def wrapper(interface_controller: InterfaceController):
        patient = interface_controller._get_patient()
        assert patient is not None, f"По id {test_consts.USER_ID_INPUT} не найдено пациента"
        assert patient.patient_id == int(test_consts.USER_ID_INPUT), "Метод вернул пациента с неправильным id"

    return wrapper


@staticmethod
def mock_get_user_id_wrong_input_1(text: str):
    assert text == consts.INPUT_PATIENT_ID_COMMAND_TEXT, "Неверный текст для ввода id пациента"
    return test_consts.USER_ID_INPUT_WRONG_1


@staticmethod
def mock_get_user_id_wrong_input_2(text: str):
    assert text == consts.INPUT_PATIENT_ID_COMMAND_TEXT, "Неверный текст для ввода id пациента"
    return test_consts.USER_ID_INPUT_WRONG_2


@staticmethod
def mock_wrong_patient_id_output_check(text: str):
    assert text == consts.PATIENT_ID_INPUT_TEXT, "Неверный вывод в консоль после ошибочного ввода id пациента"


@fixture
def check_get_patient_with_wrong_id():

    def wrapper(interface_controller: InterfaceController):
        patient = interface_controller._get_patient()
        assert patient is None, "По неверному вводу пользователя найден пациент"

    return wrapper


@staticmethod
def mock_get_input_command_stop_en(text: str):
    return consts.STOP_CMD_EN


@staticmethod
def mock_get_input_command_stop_ru(text: str):
    return consts.STOP_CMD_RU


@fixture
def check_stop_command_actions():

    def wrapper(interface_controller: InterfaceController):
        with raises(SystemExit) as exit_data:
            interface_controller.exec_command()
        assert exit_data.type == SystemExit
        assert exit_data.value.code == 0

    return wrapper
