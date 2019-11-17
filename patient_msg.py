import json
import yaml
from constants import MESSAGE_SIZE
import constants
from constants import TYPE

# Message Type
REGISTER = "patient_register"
REGISTER_RESPONSE = "patient_register_response"
SEEK_TREATMENT = "seek_treatment"
SEEK_TREATMENT_RESPONSE = "seek_treatment_response"


# Params
PATIENT_NAME = "patient_name"
PATIENT_ID = "patient_id"
RESPONSE = "response"
CARD_PATH = "card_path"

def register_msg(patient_name, patient_id):
    message = {TYPE: REGISTER, PATIENT_NAME: patient_name, PATIENT_ID: patient_id}
    return json.dumps(constants.serialize(message))

def register_response_msg(bool):
    message = {TYPE: REGISTER_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))

def seek_treatment_msg(card_path):
    message = {TYPE: SEEK_TREATMENT, CARD_PATH: card_path}
    return json.dumps(constants.serialize(message))

def seek_treatment_msg_response(bool):
    message = {TYPE: SEEK_TREATMENT_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))
