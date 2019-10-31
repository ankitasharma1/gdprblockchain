class Patient:
    def __init__(self, name, gov_id):
        self.name = name
        self.gov_id = gov_id
        self.uid = gov_id + name
        # TODO: Stretch Goal
        self.record_path = None
        self.card_path = None


class Card:
    def __init__(self, path):
        self.path = path
        self. populate()
        self.priv_key = None
        self.uid = None
        self.hospital_id = None

    def populate():
        # TODO: Open the path and populate card params

class MedicalRecord:
    def __init__(self):
    