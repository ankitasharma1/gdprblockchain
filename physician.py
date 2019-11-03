class Physician():
    def __init__(self, name, physician_id):
        self.name = name
        self.physician_id = physician_id
        self.hospital = None

    def check_in(self, hospital):
        if hospital.register_physician(self.physician_id):
            self.hospital = hospital 

    def seek_treatment(self, card):
        
