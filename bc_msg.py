import json
import yaml

# Message Type
TYPE = "type"
CONTAINS_HASH_UID = "contains_hash_uid"
GET_BLOCK = "get_block"
NEW_TXN = "new_txn"
MINE = "mine"

MESSAGE_SIZE = 128
NOP = "x"

# Params
HASH_UID = "hash_uid"
PUB_KEY = "pub_key"

# Misc.
PADDING = "padding"

def contains_hash_uid_msg(hash_uid):
    message = {TYPE: CONTAINS_HASH_UID, HASH_UID: hash_uid}
    return json.dumps(serialize(message))

def get_block(hash_uid):
    message = {TYPE: GET_BLOCK, HASH_UID: hash_uid}
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
    while i < MESSAGE_SIZE:
        message.update({PADDING: padding * i})
        if len(json.dumps(message)) == MESSAGE_SIZE:
            return message
        i = i + 1

def deserialize(message):
    return yaml.safe_load_all(message)
