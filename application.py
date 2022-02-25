from communications_controller import CommunicationsController, CommandTypes
from hospital_controller import HospitalController


class Application:

    def __init__(self, communications_controller=None, hospital_controller=None):
        self._communications_controller = (
            communications_controller if communications_controller is not None else CommunicationsController()
        )
        self._hospital_controller = hospital_controller if hospital_controller is not None else HospitalController()

    def exec_command_loop(self):
        while True:
            command = self._communications_controller.get_command()
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
                self._communications_controller.print_end_session()
                break
