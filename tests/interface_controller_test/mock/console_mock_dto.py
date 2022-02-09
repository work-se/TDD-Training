from dataclasses import dataclass


@dataclass(frozen=True)
class ExpectedInputDto:
    text: str  # выводимый пользователю текст перед вводом
    input: str
