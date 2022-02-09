from hospital import Hospital
from tests.hostpital_tests.dto import ExpectedPatientsCompoundDto


DEFAULT_PATIENT_STATUS = 1
PATIENT_TO_ADD = ExpectedPatientsCompoundDto(patient_id=1, status=DEFAULT_PATIENT_STATUS)

# несколько пациентов с одним статусом болезни
PATIENTS_TUPLE_1 = (
    ExpectedPatientsCompoundDto(patient_id=1, status=DEFAULT_PATIENT_STATUS),
    ExpectedPatientsCompoundDto(patient_id=2, status=DEFAULT_PATIENT_STATUS)
)

# несколько пациентов с различными статусами болезней (половина статусов)
PATIENTS_TUPLE_2 = tuple(
    ExpectedPatientsCompoundDto(patient_id=idx+1, status=status)
    for idx, status in enumerate(
        list(Hospital.PATIENT_STATUSES.keys())[:len(Hospital.PATIENT_STATUSES) // 2]
    )
)

# несколько пациентов с различными статусами болезней и статусы повторяются
PATIENTS_TUPLE_3 = PATIENTS_TUPLE_2[:] * 2

# пациенты со всеми возможными статусами болезней
PATIENTS_TUPLE_4 = tuple(
    ExpectedPatientsCompoundDto(patient_id=idx+1, status=status)
    for idx, status in enumerate(Hospital.PATIENT_STATUSES.keys())
)
