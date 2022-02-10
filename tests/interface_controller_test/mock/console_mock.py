from loguru import logger

from console import AbstractConsole
from tests.interface_controller_test.mock.console_mock_dto import ExpectedInputDto


class ConsoleMock(AbstractConsole):

    def __init__(self,):
        self.current_input_mock_number = 0
        self.expected_input_mock_list = []

        self.current_print_mock_number = 0
        self.expected_output_mock_list = []

    def add_expected_input(self, expected_text: str, expected_input: str):
        self.expected_input_mock_list.append(
            ExpectedInputDto(text=expected_text, input=expected_input)
        )

    def add_expected_output(self, output: str):
        self.expected_output_mock_list.append(output)

    def _use_next_input_mock(self):
        self.current_input_mock_number += 1

    def _get_current_input_mock(self) -> ExpectedInputDto:
        assert self.current_input_mock_number < len(self.expected_input_mock_list), \
            "Неожиданный запрос ввода (mock на этот вызов отсутствует)"
        return self.expected_input_mock_list[self.current_input_mock_number]

    def _get_expected_input_text(self) -> str:
        expected_input_mock = self._get_current_input_mock()
        return expected_input_mock.text

    def _get_expected_input(self) -> str:
        expected_input_mock = self._get_current_input_mock()
        return expected_input_mock.input

    def input(self, text):
        logger.debug("Call mocked 'input' - {}, {}", self.expected_input_mock_list, self.current_input_mock_number)
        expected_text = self._get_expected_input_text()
        expected_input = self._get_expected_input()
        logger.debug("expected_text={}, expected_input={}", expected_text, expected_input)
        self._use_next_input_mock()
        assert text == expected_text, "Неверный текст перед пользовательским вводом в консоль"
        return expected_input

    def _use_next_print_mock(self):
        self.current_print_mock_number += 1

    def _get_expected_print_mock(self) -> str:
        assert self.current_print_mock_number < len(self.expected_output_mock_list), \
            "Неожиданный запрос вывода (mock на этот вызов отсутствует)"
        return self.expected_output_mock_list[self.current_print_mock_number]

    def print(self, text):
        logger.debug("Call mocked 'print'")
        expected_text = self._get_expected_print_mock()
        logger.debug("expected_text={}", expected_text)
        self._use_next_print_mock()
        assert text == expected_text, "Неверный текст выводится в консоль"
