import json
import yaml
from constants import MESSAGE_SIZE
import constants
from constants import TYPE
from constants import MESSAGE_SIZE
import constants

# Message Type
REGISTER = "phys_register"
REGISTER_RESPONSE = "phys_register_response"
WRITE = "write"
WRITE_RESPONSE = "write_response"

# Params
PHYSICIAN_NAME = "physician_name"
PHYSICIAN_ID = "physician_id"
RESPONSE = "response"
CARD_PATH = "card_path"
MEDICAL_RECORD = "medical_record"
PHYS_ID = "physician_id"

def register_msg(physician_name, physician_id):
    message = {TYPE: REGISTER, PHYSICIAN_NAME: physician_name, PHYSICIAN_ID: physician_id}
    return json.dumps(constants.serialize(message))

def register_response_msg(bool):
    message = {TYPE: REGISTER_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))

def write_msg(card_path, medical_record, physician_id):
    message = {TYPE: WRITE, CARD_PATH: card_path, MEDICAL_RECORD: medical_record, PHYS_ID: physician_id}
    return json.dumps(constants.serialize(message))

def get_note_msg_length(card_path, medical_record, physician_id):
    message = {TYPE: WRITE, CARD_PATH: card_path, MEDICAL_RECORD: medical_record, PHYS_ID: physician_id}
    return MESSAGE_SIZE - len(json.dumps(message))

def write_response_msg(bool):
    message = {TYPE: WRITE_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))


