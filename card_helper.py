from hospital import Card


PATIENT_NAME = 0
PATIENT_ID = 1
UID = 2
PRIV_KEY = 3
HOSP_NAME = 4
CARD_PARAMS = 5

def get_card_object(path):
    """
    Translate contents in card path to card object
    :param path: Path where card contents are contained
    :return: card object
    """
    with open(path, "r") as filestream:
        for line in filestream:
            contents = line.split(",")
            if len(contents) != CARD_PARAMS:
                print("ERROR: incorrect card content in file")
                return None
            return Card(contents[PATIENT_NAME], contents[PATIENT_ID], contents[UID], contents[PRIV_KEY], contents[HOSP_NAME])

