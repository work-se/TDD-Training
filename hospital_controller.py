from console import AbstractConsole, Console
from communications_controller import CommunicationsController
from hospital import Hospital
from hospital import PatientDoesNotExists, PatientAlreadyWithMinStatus


class HospitalController:

    def __init__(self, console: AbstractConsole = None, hospital: Hospital = None):
        self._console = console if console is not None else Console()
        self._hospital = hospital if hospital is not None else Hospital()
        self._communication_controller = CommunicationsController(self._console)

    def decrease_patient_status(self):
        patient_id = self._communication_controller.get_patient_id()
        if patient_id is None:
            return
        try:
            self._hospital.decrease_patient_status(patient_id)
            status = self._hospital.get_patient_status_name(patient_id)
            self._communication_controller.print_change_patient_status(status)
        except (PatientAlreadyWithMinStatus, PatientDoesNotExists) as exception:
            self._communication_controller.print_exception(str(exception))

    def _discharge_patient(self, patient_id: int):
        discharge_patient = self._communication_controller.ask_confirm_discharge_patient()
        if discharge_patient:
            self._hospital.discharge_patient(patient_id)
            self._communication_controller.print_patient_discharged()
            return

        status = self._hospital.get_patient_status_name(patient_id)
        self._communication_controller.print_patient_status_not_changed(status)

    def increase_patient_status(self):
        patient_id = self._communication_controller.get_patient_id()
        if patient_id is None:
            return
        try:
            if not self._hospital.can_increase_patient_status(patient_id):
                self._discharge_patient(patient_id)
                return
            self._hospital.increase_patient_status(patient_id)
            status = self._hospital.get_patient_status_name(patient_id)
            self._communication_controller.print_change_patient_status(status)
        except PatientDoesNotExists as exception:
            self._communication_controller.print_exception(str(exception))

    def get_patient_status(self):
        patient_id = self._communication_controller.get_patient_id()
        if patient_id is None:
            return
        try:
            status = self._hospital.get_patient_status_name(patient_id)
            self._communication_controller.print_current_patient_status(status)
        except PatientDoesNotExists as exception:
            self._communication_controller.print_exception(str(exception))

    def print_statistics(self,):
        # не выводим статистику по статусам болезни, на которых нет пациентов
        stat_to_print = list(
            filter(lambda stat: stat.patients_count > 0, self._hospital.get_statistics())
        )
        self._communication_controller.print_hospital_statistics(stat_to_print)
