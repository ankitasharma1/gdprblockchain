import json
import yaml
from constants import MESSAGE_SIZE

"""
Blockchain Message Protocol Definitions/Methods.
"""

# Message Type
TYPE = "type"
CONTAINS_HASH_UID = "contains_hash_uid"
CONTAINS_HASH_UID_RESPONSE = "contains_hash_uid_response"
GET_PUB_KEY = "get_pub_key"
GET_PUB_KEY_RESPONSE = "get_pub_key_response"
NEW_TXN = "new_txn"
MINE = "mine"

NOP = "x"

# Params
HASH_UID = "hash_uid"
PUB_KEY = "pub_key"
RESPONSE = "response"

# Misc.
PADDING = "padding"

def contains_hash_uid_msg(hash_uid):
    message = {TYPE: CONTAINS_HASH_UID, HASH_UID: hash_uid}
    return json.dumps(serialize(message))

def contains_hash_uid_msg_response(response):
    message = {TYPE: CONTAINS_HASH_UID_RESPONSE, RESPONSE: response}
    return json.dumps(serialize(message))

def get_pub_key(hash_uid):
    message = {TYPE: GET_PUB_KEY, HASH_UID: hash_uid}
    return json.dumps(serialize(message))

# Deprecated - pub_keys are not json serializable.
def get_pub_key_response(response):
    message = {TYPE: GET_PUB_KEY, RESPONSE: response}
    return json.dumps(serialize(message))

def new_txn(hash_uid, pub_key):
    message = {TYPE: NEW_TXN, HASH_UID: hash_uid, PUB_KEY: pub_key}
    return json.dumps(serialize(message))

def mine():
    message = {TYPE: MINE}
    return json.dumps(serialize(message))



def bc_expecting_pub_key(messages):
    for message in messages:
        if message.get(TYPE) == NEW_TXN:
            return True
        return False

def hosp_expecting_pub_key(messages):
    for message in messages:
        if message.get(TYPE) == GET_PUB_KEY:
            return True
        return False

def requires_response(messages):
    for message in messages:
        if message.get(TYPE) == CONTAINS_HASH_UID or message.get(TYPE) == GET_PUB_KEY:
            return True
        return False

def serialize(message):
    i = 0
    padding = NOP
    if (len(json.dumps(message)) > MESSAGE_SIZE):
        print("ERROR: unable to serialize message")
        return message
    while i < MESSAGE_SIZE:
        message.update({PADDING: padding * i})
        if len(json.dumps(message)) == MESSAGE_SIZE:
            return message
        i = i + 1

def deserialize(message):
    return yaml.safe_load_all(message)

