# hospital
DISEASE_STATUSES = {
    0: "Тяжело болен", 
    1: "Болен", 
    2: "Слегка болен", 
    3: "Готов к выписке"
}
DISEASE_STATUSES_REVERSED = {value: key for key, value in DISEASE_STATUSES.items()}

DEFAULT_DISEASE_ID = 1


# commands
STOP_CMD_RU = "стоп"
STOP_CMD_EN = "stop"

STAT_CMD_RU = "рассчитать статистику"
STAT_CMD_EN = "calculate statistics"

DECREASE_PATIENT_STAT_CMD_RU = "понизить статус пациента"
DECREASE_PATIENT_STAT_CMD_EN = "status down"
INCREASE_PATIENT_STAT_CMD_RU = "повысить статус пациента"
INCREASE_PATIENT_STAT_CMD_EN = "status up"
GET_PATIENT_STAT_CMD_RU = "узнать статус пациента"
GET_PATIENT_STAT_CMD_EN = "get id"
