import pytest

from tests.mocks.console_mock import ConsoleMock


def test_add_expected_input():
    console_mock = ConsoleMock()

    console_mock.add_expected_input(expected_text="test text 1", expected_input="test input 1")
    console_mock.add_expected_input("test text 2", "test input 2")

    assert len(console_mock.expected_input_mock_list) == 2, "Сохранено неверное количество input моков"

    expected_data_1 = console_mock.expected_input_mock_list[0]
    assert expected_data_1.text == "test text 1", "Сохранен неверный текст для input mock 1"
    assert expected_data_1.input == "test input 1", "Сохранен неверный input для input mock 1"

    expected_data_2 = console_mock.expected_input_mock_list[1]
    assert expected_data_2.text == "test text 2", "Сохранен неверный текст для input mock 2"
    assert expected_data_2.input == "test input 2", "Сохранен неверный input для input mock 2"


def test_add_expected_print():
    console_mock = ConsoleMock()

    console_mock.add_expected_print(print_text="test print 1")
    console_mock.add_expected_print("test print 2")

    assert len(console_mock.expected_print_mock_list) == 2, "Сохранено неверное количество print моков"

    expected_print_1 = console_mock.expected_print_mock_list[0]
    assert expected_print_1 == "test print 1", "Сохранен неверный текст для print mock 1"

    expected_print_2 = console_mock.expected_print_mock_list[1]
    assert expected_print_2 == "test print 2", "Сохранен неверный текст для print mock 2"


def test_get_current_input_mock():
    console_mock = ConsoleMock()

    console_mock.add_expected_input(expected_text="test text 1", expected_input="test input 1")
    console_mock.add_expected_input("test text 2", "test input 2")

    text, input = console_mock._get_current_input_mock()
    assert text == "test text 1", "Получен неверный mock текста для input"
    assert input == "test input 1", "Получен неверный mock input"
    assert len(console_mock.expected_input_mock_list) == 1, "Мок не был удален после применения"

    text, input = console_mock._get_current_input_mock()
    assert text == "test text 2", "Получен неверный mock текста для input"
    assert input == "test input 2", "Получен неверный mock input"
    assert len(console_mock.expected_input_mock_list) == 0, "Мок не был удален после применения"


def test_get_current_empty_input_mock():
    console_mock = ConsoleMock()

    with pytest.raises(AssertionError) as exception:
        console_mock._get_current_input_mock()
    assert "Неожиданный запрос ввода (mock на этот вызов отсутствует)" in str(exception.value), \
        "Нет ожидаемого сообщения об ошибке при получении мока"


def test_get_current_print_mock():
    console_mock = ConsoleMock()

    console_mock.add_expected_print(print_text="test print 1")
    console_mock.add_expected_print("test print 2")

    text = console_mock._get_current_print_mock()
    assert text == "test print 1", "Получен неверный mock текста для input"
    assert len(console_mock.expected_print_mock_list) == 1, "Мок не был удален после применения"

    text = console_mock._get_current_print_mock()
    assert text == "test print 2", "Получен неверный mock текста для input"
    assert len(console_mock.expected_print_mock_list) == 0, "Мок не был удален после применения"


def test_get_current_empty_print_mock():
    console_mock = ConsoleMock()

    with pytest.raises(AssertionError) as exception:
        console_mock._get_current_print_mock()
    assert "Неожиданный запрос вывода (mock на этот вызов отсутствует)" in str(exception.value), \
        "Нет ожидаемого сообщения об ошибке при получении мока"


def test_input_mock():
    console_mock = ConsoleMock()
    console_mock.add_expected_input(expected_text="test text", expected_input="test input")

    try:
        input = console_mock.input("test text")
    except AssertionError:
        assert False, "Ложное срабатывание проверки корректности текста input"
    assert input == "test input", "Неверный input получен из mock-метода"
    assert len(console_mock.expected_input_mock_list) == 0, "Мок не был удален после применения"


def test_input_mock_with_error_input_text():
    console_mock = ConsoleMock()
    console_mock.add_expected_input(expected_text="test text", expected_input="test input")

    with pytest.raises(AssertionError):
        console_mock.input("test error text")


def test_print_mock():
    console_mock = ConsoleMock()
    console_mock.add_expected_print(print_text="test print")

    try:
        console_mock.print("test print")
    except AssertionError:
        assert False, "Ложное срабатывание проверки корректности текста print"
    assert len(console_mock.expected_input_mock_list) == 0, "Мок не был удален после применения"


def test_print_mock_with_error_print_text():
    console_mock = ConsoleMock()
    console_mock.add_expected_print(print_text="test print")

    with pytest.raises(AssertionError):
        console_mock.print("test error print")


def test_check_all_mocks_used():
    console_mock = ConsoleMock()
    console_mock.add_expected_input(expected_text="test text", expected_input="test input")
    console_mock.add_expected_print(print_text="test print")

    with pytest.raises(AssertionError) as exception:
        console_mock.check_all_mocks_used()
    assert "Использованы не все ожидаемые моки ввода" == str(exception.value), \
        "Неожиданный текст исключения при проверке"

    console_mock.expected_input_mock_list.pop(0)
    with pytest.raises(AssertionError) as exception:
        console_mock.check_all_mocks_used()
    assert "Использованы не все ожидаемые моки вывода" == str(exception.value), \
        "Неожиданный текст исключения при проверке"

    console_mock.expected_print_mock_list.pop(0)
    try:
        console_mock.check_all_mocks_used()
    except AssertionError:
        assert False, "Ложное срабатывание проверки использования всех ожидаемых моков"
