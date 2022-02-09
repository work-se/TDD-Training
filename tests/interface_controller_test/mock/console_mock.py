from loguru import logger

from console import Console
from tests.interface_controller_test.mock.console_mock_dto import ExpectedInputDto


class ConsoleMock:

    def __init__(self, monkeypatch):
        self.monkey_patch = monkeypatch

        self.current_input_mock_number = 0
        self.expected_input_mock_list = []

        self.current_output_mock_number = 0
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
        return self.expected_input_mock_list[self.current_input_mock_number]

    def _get_expected_input_text(self) -> str:
        expected_input_mock = self._get_current_input_mock()
        return expected_input_mock.text

    def _get_expected_input(self) -> str:
        expected_input_mock = self._get_current_input_mock()
        return expected_input_mock.input

    def mock_get_input(self):
        def mock(text: str):
            logger.debug("Call mocked 'get_input'")
            expected_text = self._get_expected_input_text()
            expected_input = self._get_expected_input()
            logger.debug("expected_text={}, expected_input={}", expected_text, expected_input)
            self._use_next_input_mock()
            assert text == expected_text, "Неверный текст перед пользовательским вводом в консоль"
            return expected_input
        self.monkey_patch.setattr(Console, "get_input", staticmethod(mock))

    def _use_next_output_mock(self):
        self.current_output_mock_number += 1

    def _get_expected_output_mock(self) -> str:
        return self.expected_output_mock_list[self.current_output_mock_number]

    def mock_put_output(self):
        def mock(text: str):
            logger.debug("Call mocked 'put_output'")
            expected_text = self._get_expected_output_mock()
            logger.debug("expected_text={}", expected_text)
            self._use_next_output_mock()
            assert text == expected_text, "Неверный текст выводится в консоль"
        self.monkey_patch.setattr(Console, "put_output", staticmethod(mock))
