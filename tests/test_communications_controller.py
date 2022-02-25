import pytest

from communications_controller import CommunicationsController, CommandTypes, ReceivedInvalidId
from dtos.statistics_dto import StatisticsDto
from tests.mocks.console_mock import ConsoleMock


# Здесь почти unit-тесты (используется только ConsoleMock)


def test_command_types_parse_str_commands():
    assert CommandTypes("stop") == CommandTypes.STOP, "По английской строке определена неверная команда"
    assert CommandTypes("стоп") == CommandTypes.STOP, "По русской строке определена неверная команда"


@pytest.mark.parametrize(
    "en_command,ru_command,expected_type",
    (
        ("stop", "стоп", CommandTypes.STOP),
        ("calculate statistics", "рассчитать статистику", CommandTypes.CALCULATE_STAT),
        ("status down", "понизить статус пациента", CommandTypes.DECREASE_PATIENT_STAT),
        ("status up", "повысить статус пациента", CommandTypes.INCREASE_PATIENT_STAT),
        ("get id", "узнать статус пациента", CommandTypes.GET_PATIENT_STAT),
    )
)
def test_command_types_internal_logic(en_command, ru_command, expected_type):
    assert en_command in CommandTypes._value2member_map_, \
        "Нет английского текста команды в списке доступных для парсинга команд"
    assert ru_command in CommandTypes._value2member_map_, \
        "Нет русского текста команды в списке доступных для парсинга команд"
    assert CommandTypes(en_command) == CommandTypes(ru_command), \
        "Английский и русский версии команды ведут на разный enum instance"
    assert CommandTypes(en_command) == expected_type, "По команде получен enum instance отличный от ожидаемого"


@pytest.mark.parametrize(
    "command,expected_command",
    (
        ("stop", CommandTypes.STOP), ("стоп", CommandTypes.STOP),
        ("calculate statistics", CommandTypes.CALCULATE_STAT),
        ("рассчитать статистику", CommandTypes.CALCULATE_STAT),
        ("status down", CommandTypes.DECREASE_PATIENT_STAT),
        ("понизить статус пациента", CommandTypes.DECREASE_PATIENT_STAT),
        ("status up", CommandTypes.INCREASE_PATIENT_STAT),
        ("повысить статус пациента", CommandTypes.INCREASE_PATIENT_STAT),
        ("get id", CommandTypes.GET_PATIENT_STAT), ("узнать статус пациента", CommandTypes.GET_PATIENT_STAT),
    )
)
def test_get_command(command, expected_command):
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)

    parsed_command = communications_controller.get_command()
    assert parsed_command == expected_command, "Текст преобразован в неверную команду"
    console_mock.check_all_mocks_used()


def test_get_wrong_command():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="wrong command")
    console_mock.add_expected_print(print_text="Неизвестная команда! Попробуйте ещё раз.")

    parsed_command = communications_controller.get_command()
    assert parsed_command is None, "Неизвестная команда преобразована в какую-то из известных команд"
    console_mock.check_all_mocks_used()


def test_get_patient_id():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")

    patient_id = communications_controller.get_patient_id()
    assert patient_id == 1, "Получен неожиданный id пациента"
    console_mock.check_all_mocks_used()


@pytest.mark.parametrize(
    "wrong_id", ("asd", "1.2", "1,2")
)
def test_get_wrong_patient_id(wrong_id):
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input=wrong_id)

    with pytest.raises(ReceivedInvalidId) as exception:
        communications_controller.get_patient_id()
    assert "Ошибка ввода. ID пациента должно быть числом (целым, положительным)" == str(exception.value), \
        "Неожиданный текст ошибки"
    console_mock.check_all_mocks_used()


def test_confirm_discharge_patient():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)

    console_mock.add_expected_input(expected_text="Желаете этого пациента выписать? (да/нет)", expected_input="да")
    answer = communications_controller.request_confirm_discharge_patient()
    assert answer is True, "Неверно интерпретировано подтверждение выписки пациента"
    console_mock.check_all_mocks_used()


def test_not_confirm_discharge_patient():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "нет")
    answer = communications_controller.request_confirm_discharge_patient()
    assert answer is False, "Неверно интерпретировано подтверждение выписки пациента"
    console_mock.check_all_mocks_used()


def test_print_change_patient_status():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(print_text="Новый статус пациента: Новый статус")

    communications_controller.print_change_patient_status("Новый статус")
    console_mock.check_all_mocks_used()


def test_print_current_patient_status():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(print_text="Статус пациента: Текущий статус")

    communications_controller.print_current_patient_status("Текущий статус")
    console_mock.check_all_mocks_used()


def test_print_end_session():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(print_text="Сеанс завершён.")

    communications_controller.print_end_session()
    console_mock.check_all_mocks_used()


def test_print_hospital_statistics():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    statuses = [
        StatisticsDto(status_name="Болен", patients_count=199),
        StatisticsDto(status_name="Готов к выписке", patients_count=1)
    ]

    console_mock.add_expected_print(print_text="Статистика по статусам:")
    console_mock.add_expected_print(print_text='- в статусе "Болен": 199 чел.')
    console_mock.add_expected_print(print_text='- в статусе "Готов к выписке": 1 чел.')

    communications_controller.print_hospital_statistics(statuses)
    console_mock.check_all_mocks_used()


def test_print_patients_cant_die():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(
        print_text="Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)"
    )

    communications_controller.print_patients_cant_die()
    console_mock.check_all_mocks_used()


def test_print_patient_discharged():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(print_text="Пациент выписан из больницы")

    communications_controller.print_patient_discharged()
    console_mock.check_all_mocks_used()


def test_print_patient_status_not_changed():
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    console_mock.add_expected_print(print_text='Пациент остался в статусе "Текущий статус"')

    communications_controller.print_patient_status_not_changed("Текущий статус")
    console_mock.check_all_mocks_used()
