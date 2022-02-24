from application import Application
from communications_controller import CommunicationsController
from hospital_controller import HospitalController
from tests.mocks.console_mock import ConsoleMock


def test_complex_script_iteration_1_num_1():
    """
    Тестовый сценарий № 1 (стандартный)
    сценарий из файла tasks/Тренинг_по_архитектуре_итерация_1.md
    """
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="узнать статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Статус пациента: Болен")

    console_mock.add_expected_input("Введите команду: ", "повысить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "2")
    console_mock.add_expected_print("Новый статус пациента: Слегка болен")

    console_mock.add_expected_input("Введите команду: ", "понизить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "3")
    console_mock.add_expected_print("Новый статус пациента: Тяжело болен")

    console_mock.add_expected_input("Введите команду: ", "рассчитать статистику")
    console_mock.add_expected_print("Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Болен": 198 чел.')
    console_mock.add_expected_print('- в статусе "Слегка болен": 1 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()


def test_complex_script_iteration_2_num_1():
    """
    Итерация № 2
    Тестовый сценарий № 1
    попытка повысить самый высокий статус, которая приводит к выписке пациента
    сценарий из файла tasks/Тренинг_по_архитектуре_итерация_2.md
    """
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="повысить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "200")
    console_mock.add_expected_print(print_text="Новый статус пациента: Слегка болен")

    console_mock.add_expected_input("Введите команду: ", "повысить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "200")
    console_mock.add_expected_print("Новый статус пациента: Готов к выписке")

    console_mock.add_expected_input("Введите команду: ", "повысить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "200")
    console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "да")
    console_mock.add_expected_print("Пациент выписан из больницы")

    console_mock.add_expected_input("Введите команду: ", "рассчитать статистику")
    console_mock.add_expected_print("Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Болен": 199 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()


def test_complex_script_iteration_2_num_2():
    """
    Итерация № 2
    Тестовый сценарий № 1
    попытка повысить самый высокий статус, которая ни к чему не приводит
    сценарий из файла tasks/Тренинг_по_архитектуре_итерация_2.md
    """
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="повысить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "200")
    console_mock.add_expected_print(print_text="Новый статус пациента: Слегка болен")

    console_mock.add_expected_input("Введите команду: ", "повысить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "200")
    console_mock.add_expected_print("Новый статус пациента: Готов к выписке")

    console_mock.add_expected_input("Введите команду: ", "повысить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "200")
    console_mock.add_expected_input("Желаете этого пациента выписать? (да/нет)", "нет")
    console_mock.add_expected_print('Пациент остался в статусе "Готов к выписке"')

    console_mock.add_expected_input("Введите команду: ", "рассчитать статистику")
    console_mock.add_expected_print("Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Болен": 199 чел.')
    console_mock.add_expected_print('- в статусе "Готов к выписке": 1 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()


def test_complex_script_iteration_2_num_3():
    """
    Итерация № 2
    Тестовый сценарий № 1
    неудачная попытка понизить самый низкий статус
    сценарий из файла tasks/Тренинг_по_архитектуре_итерация_2.md
    """
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="понизить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print(print_text="Новый статус пациента: Тяжело болен")

    console_mock.add_expected_input("Введите команду: ", "понизить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    console_mock.add_expected_input("Введите команду: ", "узнать статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "1")
    console_mock.add_expected_print("Статус пациента: Тяжело болен")

    console_mock.add_expected_input("Введите команду: ", "рассчитать статистику")
    console_mock.add_expected_print("Статистика по статусам:")
    console_mock.add_expected_print('- в статусе "Тяжело болен": 1 чел.')
    console_mock.add_expected_print('- в статусе "Болен": 199 чел.')

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()


def test_complex_script_iteration_2_num_4():
    """
    Итерация № 2
    Тестовый сценарий № 1
    случаи ввода пользователем некорректных данных
    сценарий из файла tasks/Тренинг_по_архитектуре_итерация_2.md
    """
    console_mock = ConsoleMock()
    communications_controller = CommunicationsController(console_mock)
    hospital_controller = HospitalController(communications_controller)
    application = Application(communications_controller, hospital_controller)

    console_mock.add_expected_input(expected_text="Введите команду: ", expected_input="узнать статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "два")
    console_mock.add_expected_print(print_text="Ошибка ввода. ID пациента должно быть числом (целым, положительным)")

    console_mock.add_expected_input("Введите команду: ", "понизить статус пациента")
    console_mock.add_expected_input("Введите ID пациента: ", "201")
    console_mock.add_expected_print(print_text="Ошибка. В больнице нет пациента с таким ID")

    console_mock.add_expected_input("Введите команду: ", "stop")
    console_mock.add_expected_print("Сеанс завершён.")

    application.exec_command_loop()
    console_mock.check_all_mocks_used()
