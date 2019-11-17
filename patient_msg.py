import json
import yaml
from constants import MESSAGE_SIZE
import constants

# Message Type
TYPE = "type"
REGISTER = "register"

# Params
PATIENT_NAME = "patient_name"
PATIENT_ID = "patient_id"

def register_msg(patient_name, patient_id):
    message = {TYPE: REGISTER, PATIENT_NAME: patient_name, PATIENT_ID: patient_id}
    return json.dumps(constants.serialize(message))

