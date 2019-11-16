import json
import yaml

# Message Type
TYPE = "type"

MESSAGE_SIZE = 256
NOP = "x"

# Misc.
PADDING = "padding"

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

