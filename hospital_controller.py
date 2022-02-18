from console import AbstractConsole, Console
from communications_controller import CommunicationsController, ReceivedInvalidId
from hospital import Hospital
from hospital import PatientDoesNotExists, PatientAlreadyWithMinStatus, PatientAlreadyWithMaxStatus


def catch_patient_does_not_exists(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except PatientDoesNotExists as exception:
            self._console.print(str(exception))

    return wrapper


def catch_with_invalid_id(func):

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ReceivedInvalidId:
            pass

    return wrapper


class HospitalController:

    def __init__(self, console: AbstractConsole, hospital: Hospital):
        self._console = console
        self._hospital = hospital
        self._communication_controller = CommunicationsController(self._console)

    @catch_patient_does_not_exists
    @catch_with_invalid_id
    def decrease_patient_status(self):
        patient_id = self._communication_controller.get_patient_id()
        try:
            self._hospital.decrease_patient_status(patient_id=patient_id)
            status = self._hospital.get_patient_status_name(patient_id)
            self._communication_controller.print_change_patient_status(status)
        except PatientAlreadyWithMinStatus:
            self._communication_controller.print_patients_cant_die()

    def _discharge_patient(self, patient_id: int):
        discharge_patient = self._communication_controller.ask_confirm_discharge_patient()
        if discharge_patient:
            self._hospital.discharge_patient(patient_id)
            self._communication_controller.print_patient_discharged()
            return

        status = self._hospital.get_patient_status_name(patient_id)
        self._communication_controller.print_patient_status_not_changed(status)

    @catch_patient_does_not_exists
    @catch_with_invalid_id
    def increase_patient_status(self):
        patient_id = self._communication_controller.get_patient_id()
        try:
            self._hospital.increase_patient_status(patient_id)
            status = self._hospital.get_patient_status_name(patient_id)
            self._communication_controller.print_change_patient_status(status)
        except PatientAlreadyWithMaxStatus:
            self._discharge_patient(patient_id)

    @catch_patient_does_not_exists
    @catch_with_invalid_id
    def get_patient_status(self):
        patient_id = self._communication_controller.get_patient_id()
        status = self._hospital.get_patient_status_name(patient_id)
        self._communication_controller.print_current_patient_status(status)

    def print_statistics(self,):
        # не выводим статистику по статусам болезни, на которых нет пациентов
        stat_to_print = list(
            filter(lambda stat: stat.patients_count > 0, self._hospital.get_statistics())
        )
        self._communication_controller.print_hospital_statistics(stat_to_print)
