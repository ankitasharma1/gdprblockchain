import json
import yaml

# Message Type
TYPE = "type"
CONTAINS_HASH_UID = "contains_hash_uid"
CONTAINS_HASH_UID_RESPONSE = "contains_hash_uid_response"
GET_BLOCK = "get_block"
GET_BLOCK_RESPONSE = "get_block_response"
NEW_TXN = "new_txn"
MINE = "mine"

MESSAGE_SIZE = 256
NOP = "x"

# Params
HASH_UID = "hash_uid"
PUB_KEY = "pub_key"

# Misc.
PADDING = "padding"

def contains_hash_uid_msg(hash_uid):
    message = {TYPE: CONTAINS_HASH_UID, HASH_UID: hash_uid}
    return json.dumps(serialize(message))

def contains_hash_uid_msg_response(response):
    message = {TYPE: CONTAINS_HASH_UID_RESPONSE, RESPONSE: response}
    return json.dumps(serialize(message))

def get_block(hash_uid):
    message = {TYPE: GET_BLOCK, HASH_UID: hash_uid}
    return json.dumps(serialize(message))

def get_block_response(response):
    message = {TYPE: GET_BLOCK_RESPONSE, RESPONSE: response}
    return json.dumps(serialize(message))

def new_txn(hash_uid, pub_key):
    message = {TYPE: NEW_TXN, HASH_UID: hash_uid, PUB_KEY: pub_key}
    return json.dumps(serialize(message))

def mine():
    message = {TYPE: MINE}
    return json.dumps(serialize(message))

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

def requires_response(messages):
    for message in messages:
        if message.get(TYPE) == CONTAINS_HASH_UID or message.get(TYPE) == GET_BLOCK:
            return True
        return False

def handle_response(message):
    print(message)
    if message.get(TYPE) == CONTAINS_HASH_UID or message.get(TYPE) == GET_BLOCK:
        return message.get(RESPONSE)
    return None
