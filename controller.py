import consts

from typing import Optional

from console import Console, AbstractConsole
from communications_controller import CommunicationsController, CommandTypes
from hospital import Hospital
from hospital_controller import HospitalController


class InterfaceController:
    PATIENT_STATUS = 1
    USERS_COUNT = 200

    def __init__(
        self, console: AbstractConsole = None, hospital: Hospital = None,
    ):
        self._hospital = self._get_hospital() if hospital is None else hospital
        self._console = Console() if console is None else console
        self._hospital_controller = HospitalController(self._console, self._hospital)
        self._communication_controller = CommunicationsController(self._console)

    def _get_hospital(self):
        hospital = Hospital()
        for i in range(self.USERS_COUNT):
            hospital.add_patient(self.PATIENT_STATUS)
        return hospital

    def exec_command(self):
        while True:
            command = self._communication_controller.get_command()
            if command is None:
                continue

            if command == CommandTypes.DECREASE_PATIENT_STAT:
                self._hospital_controller.decrease_patient_status()
            elif command == CommandTypes.INCREASE_PATIENT_STAT:
                self._hospital_controller.increase_patient_status()
            elif command == CommandTypes.GET_PATIENT_STAT:
                self._hospital_controller.get_patient_status()
            elif command == CommandTypes.CALCULATE_STAT:
                self._hospital_controller.print_statistics()
            elif command == CommandTypes.STOP:
                self._communication_controller.print_end_session()
                break
