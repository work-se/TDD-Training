import sys

from controller import InterfaceController


controller = InterfaceController()


if __name__ == "__main__":
    print("______________________")
    while True:
        controller.exec_command()
