import json
import yaml
from constants import MESSAGE_SIZE
import constants
from constants import TYPE

# Message Type
REGISTER = "register"
REGISTER_RESPONSE = "register_response"

# Params
PATIENT_NAME = "patient_name"
PATIENT_ID = "patient_id"
RESPONSE = "response"

def register_msg(patient_name, patient_id):
    message = {TYPE: REGISTER, PATIENT_NAME: patient_name, PATIENT_ID: patient_id}
    return json.dumps(constants.serialize(message))

def register_response_msg(bool):
    message = {TYPE: REGISTER_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))

