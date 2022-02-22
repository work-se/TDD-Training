from communications_controller import CommunicationsController, ReceivedInvalidId
from hospital import Hospital
from hospital import PatientDoesNotExists, PatientAlreadyWithMinStatus


class HospitalController:

    def __init__(self, communication_controller=None, hospital=None):
        self._hospital = hospital if hospital is not None else Hospital()
        self._communication_controller = (
            communication_controller if communication_controller is not None else CommunicationsController()
        )

    def decrease_patient_status(self):
        try:
            patient_id = self._communication_controller.get_patient_id()
            self._hospital.decrease_patient_status(patient_id)
            status = self._hospital.get_patient_status_name(patient_id)
            self._communication_controller.print_change_patient_status(status)
        except (PatientAlreadyWithMinStatus, PatientDoesNotExists, ReceivedInvalidId) as exception:
            self._communication_controller.print_exception(str(exception))

    def increase_patient_status(self):
        try:
            patient_id = self._communication_controller.get_patient_id()
            if self._hospital.can_increase_patient_status(patient_id):
                self._hospital.increase_patient_status(patient_id)
                status = self._hospital.get_patient_status_name(patient_id)
                self._communication_controller.print_change_patient_status(status)
            else:
                if self._communication_controller.request_confirm_discharge_patient():
                    self._hospital.discharge_patient(patient_id)
                    self._communication_controller.print_patient_discharged()
                else:
                    status = self._hospital.get_patient_status_name(patient_id)
                    self._communication_controller.print_patient_status_not_changed(status)
        except (PatientDoesNotExists, ReceivedInvalidId) as exception:
            self._communication_controller.print_exception(str(exception))

    def get_patient_status(self):
        try:
            patient_id = self._communication_controller.get_patient_id()
            status = self._hospital.get_patient_status_name(patient_id)
            self._communication_controller.print_current_patient_status(status)
        except (PatientDoesNotExists, ReceivedInvalidId) as exception:
            self._communication_controller.print_exception(str(exception))

    def print_statistics(self,):
        # не выводим статистику по статусам болезни, на которых нет пациентов
        stat_to_print = list(
            filter(lambda stat: stat.patients_count > 0, self._hospital.get_statistics())
        )
        self._communication_controller.print_hospital_statistics(stat_to_print)
