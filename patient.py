class Patient:
    def __init__(self, name, gov_id):
        self.name = name
        self.gov_id = gov_id
        self.uid = gov_id + name
        # TODO: Stretch Goal - keep track of their own records
        self.record_path = None
        self.card_path = None


class Card:
    def __init__(self, path):
        self.path = path
        self. populate()
        self.priv_key = None
        self.uid = None
        self.hospital_id = None

    def populate(self):
        # TODO: Open the path and populate card params
        pass

    def update(self, hospital_id):
        self.hospital_id = hospital_id

class MedicalRecord:
    def __init__(self):
        pass

    # REPL for commands