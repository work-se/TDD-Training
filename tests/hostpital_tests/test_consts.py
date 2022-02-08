import consts

from tests.hostpital_tests.dto import ExpectedPatientsCompoundDto


PATIENT_TO_ADD = ExpectedPatientsCompoundDto(patient_id=1, disease_id=consts.DEFAULT_DISEASE_ID)

# несколько пациентов с одним статусом болезни
PATIENTS_TUPLE_1 = (
    ExpectedPatientsCompoundDto(patient_id=1, disease_id=consts.DEFAULT_DISEASE_ID),
    ExpectedPatientsCompoundDto(patient_id=2, disease_id=consts.DEFAULT_DISEASE_ID)
)

# несколько пациентов с различными статусами болезней (половина статусов)
PATIENTS_TUPLE_2 = tuple(
    ExpectedPatientsCompoundDto(patient_id=idx+1, disease_id=disease_id)
    for idx, disease_id in enumerate(
        list(consts.DISEASE_STATUSES.keys())[:len(consts.DISEASE_STATUSES) // 2]
    )
)

# несколько пациентов с различными статусами болезней и статусы повторяются
PATIENTS_TUPLE_3 = PATIENTS_TUPLE_2[:] * 2

# пациенты со всеми возможными статусами болезней
PATIENTS_TUPLE_4 = tuple(
    ExpectedPatientsCompoundDto(patient_id=idx+1, disease_id=disease_id)
    for idx, disease_id in enumerate(consts.DISEASE_STATUSES.keys())
)
