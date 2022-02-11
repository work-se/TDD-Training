from dataclasses import dataclass
from loguru import logger
from typing import Tuple

from console import AbstractConsole


@dataclass(frozen=True)
class ExpectedInputDto:
    text: str  # выводимый пользователю текст перед вводом
    input: str


class ConsoleMock(AbstractConsole):

    def __init__(self,):
        self.expected_input_mock_list = []
        self.expected_output_mock_list = []

    def add_expected_input(self, expected_text: str, expected_input: str):
        self.expected_input_mock_list.append(
            ExpectedInputDto(text=expected_text, input=expected_input)
        )

    def add_expected_output(self, output: str):
        self.expected_output_mock_list.append(output)

    def _get_current_input_mock(self) -> Tuple[str, str]:
        assert self.expected_input_mock_list, "Неожиданный запрос ввода (mock на этот вызов отсутствует)"
        mock = self.expected_input_mock_list.pop(0)
        return mock.text, mock.input

    def input(self, text):
        logger.debug("Call mocked 'input' - {}", self.expected_input_mock_list)
        expected_text, expected_input = self._get_current_input_mock()
        logger.debug("expected_text={}, expected_input={}", expected_text, expected_input)
        assert text == expected_text, "Неверный текст перед пользовательским вводом в консоль"
        return expected_input

    def _get_expected_print_mock(self) -> str:
        assert self.expected_output_mock_list, "Неожиданный запрос вывода (mock на этот вызов отсутствует)"
        return self.expected_output_mock_list.pop(0)

    def print(self, text):
        logger.debug("Call mocked 'print'")
        expected_text = self._get_expected_print_mock()
        logger.debug("expected_text={}", expected_text)
        assert text == expected_text, "Неверный текст выводится в консоль"
