from abc import ABC, abstractmethod


class AbstractConsole(ABC):

    @staticmethod
    @abstractmethod
    def input(text: str) -> str:
        ...

    @staticmethod
    @abstractmethod
    def print(text: str):
        ...


class Console(AbstractConsole):

    @staticmethod
    def input(text: str) -> str:
        return input(text)

    @staticmethod
    def print(text: str):
        print(text)
