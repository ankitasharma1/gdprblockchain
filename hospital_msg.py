import json
import yaml
from constants import MESSAGE_SIZE
import constants
from constants import TYPE

# Message Type
TRANSFER_WRITE = "transfer_write"
TRANSFER_WRITE_RESPONSE = "transfer_write_response"

# Params
RESPONSE = "response"
BLOCK = "blk"
NUM_BLOCKS = "num_blk"
DB_KEY = "db_key"

def transfer_write_msg(db_key, block, num_blk):
    message = {TYPE: TRANSFER_WRITE, DB_KEY: db_key, BLOCK: block, NUM_BLOCKS: num_blk}
    return json.dumps(constants.serialize(message))

def transfer_write_response_msg(bool):
    message = {TYPE: TRANSFER_WRITE_RESPONSE, RESPONSE: bool}
    return json.dumps(constants.serialize(message))

