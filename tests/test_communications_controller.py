import pytest

from communications_controller import CommunicationsController, CommandTypes, ReceivedInvalidId
from dtos.statistics_dto import StatisticsDto
from tests.console_mock import ConsoleMock


@pytest.mark.parametrize(
    "command,expected_command",
    (
        ("stop", CommandTypes.STOP), ("стоп", CommandTypes.STOP),
        ("calculate statistics", CommandTypes.CALCULATE_STAT), ("рассчитать статистику", CommandTypes.CALCULATE_STAT),
        ("status down", CommandTypes.DECREASE_PATIENT_STAT),
        ("понизить статус пациента", CommandTypes.DECREASE_PATIENT_STAT),
        ("status up", CommandTypes.INCREASE_PATIENT_STAT),
        ("повысить статус пациента", CommandTypes.INCREASE_PATIENT_STAT),
        ("get id", CommandTypes.GET_PATIENT_STAT), ("узнать статус пациента", CommandTypes.GET_PATIENT_STAT),
    )
)
def test_get_command(command, expected_command):
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_input(expected_text="Введите команду: ", expected_input=command)

        parsed_command = communications_controller.get_command()
        assert parsed_command == expected_command, "Текст преобразован в неверную команду"


def test_get_wrong_command():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="wrong command")
        console_mock.add_expected_print(print_text="Неизвестная команда! Попробуйте ещё раз.")

        parsed_command = communications_controller.get_command()
        assert parsed_command is None, "Неизвестная команда преобразована в какую-то из известных команд"


def test_patient_id():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input="1")

        patient_id = communications_controller.get_patient_id()
        assert patient_id == 1, "Получен неожиданный id пациента"


@pytest.mark.parametrize(
    "wrong_id", ("asd", "1.2", "1,2")
)
def test_wrong_patient_id(wrong_id):
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_input(expected_text="Введите ID пациента: ", expected_input=wrong_id)
        console_mock.add_expected_print(
            print_text="Ошибка ввода. ID пациента должно быть числом (целым, положительным)"
        )

        with pytest.raises(ReceivedInvalidId):
            patient_id = communications_controller.get_patient_id()


def test_confirm_discharge_patient():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)

        console_mock.add_expected_input(expected_text="Желаете этого пациента выписать? (да/нет)", expected_input="да")
        answer = communications_controller.ask_confirm_discharge_patient()
        assert answer is True, "Неверно интерпретировано подтверждение выписки пациента"

        console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "нет")
        answer = communications_controller.ask_confirm_discharge_patient()
        assert answer is False, "Неверно интерпретировано подтверждение выписки пациента"


def test_print_change_patient_status():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_print(print_text="Новый статус пациента: Новый статус")

        communications_controller.print_change_patient_status("Новый статус")


def test_print_current_patient_status():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_print(print_text="Статус пациента: Текущий статус")

        communications_controller.print_current_patient_status("Текущий статус")


def test_print_end_session():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_print(print_text="Сеанс завершён.")

        communications_controller.print_end_session()


def test_print_hospital_statistics():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        statuses = [
            StatisticsDto(status_name="Болен", patients_count=199),
            StatisticsDto(status_name="Готов к выписке", patients_count=1)
        ]

        console_mock.add_expected_print(print_text="Статистика по статусам:")
        console_mock.add_expected_print(print_text='- в статусе "Болен": 199 чел.')
        console_mock.add_expected_print(print_text='- в статусе "Готов к выписке": 1 чел.')

        communications_controller.print_hospital_statistics(statuses)


def test_print_patients_cant_die():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_print(
            print_text="Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)"
        )

        communications_controller.print_patients_cant_die()


def test_print_patient_discharged():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_print(print_text="Пациент выписан из больницы")

        communications_controller.print_patient_discharged()


def test_print_patient_status_not_changed():
    with ConsoleMock() as console_mock:
        communications_controller = CommunicationsController(console_mock)
        console_mock.add_expected_print(print_text='Пациент остался в статусе "Текущий статус"')

        communications_controller.print_patient_status_not_changed("Текущий статус")
