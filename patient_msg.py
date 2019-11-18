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
READ = "read"
PHYS_READ = "phys_read"
READ_RESPONSE = "read_response"
PHYS_READ_RESPONSE = "phys_read_response"
REMOVE = "remove"
REMOVE_RESPONSE = "remove_response"


# Params
PATIENT_NAME = "patient_name"
PATIENT_ID = "patient_id"
RESPONSE = "response"
CARD_PATH = "card_path"
CARD_UID = "card_uid"
BLOCK = "blk"
NUM_BLOCKS = "num_blk"

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

def read_msg(card_uid):
    message = {TYPE: READ, CARD_UID: card_uid}
    return json.dumps(constants.serialize(message))

def read_response_msg(block, num_blk, bool):
    message = {TYPE: READ_RESPONSE, BLOCK: block, NUM_BLOCKS: num_blk, RESPONSE: bool}
    return json.dumps(constants.serialize(message))

def phys_read_msg(card_path):
    message = {TYPE: PHYS_READ, CARD_PATH: card_path}
    return json.dumps(constants.serialize(message))

def phys_read_response_msg(bool):
    message = {TYPE: PHYS_READ_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))

def remove_msg(card_path):
    message = {TYPE: REMOVE, CARD_PATH: card_path}
    return json.dumps(constants.serialize(message))

def remove_response_msg(bool):
    message = {TYPE: REMOVE_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))


