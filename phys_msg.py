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

# Params
PHYSICIAN_NAME = "physician_name"
PHYSICIAN_ID = "physician_id"
RESPONSE = "response"

def register_msg(physician_name, physician_id):
    message = {TYPE: REGISTER, PHYSICIAN_NAME: physician_name, PHYSICIAN_ID: physician_id}
    return json.dumps(constants.serialize(message))

def register_response_msg(bool):
    message = {TYPE: REGISTER_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))