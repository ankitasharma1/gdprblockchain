import yaml
import json

ERROR = -1
ADDRESS = 0
PORT = 1

TYPE = "type"

MESSAGE_SIZE = 256

# Misc.
NOP = "x"
PADDING = "padding"


# File which contains information for the world we are simulating.
CONFIG_FILE = 'config.yaml'

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

