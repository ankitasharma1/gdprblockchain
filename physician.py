from medical_record import MedicalRecord
from time import time
import crypto

class Physician():
    def __init__(self, name, physician_id):
        self.name = name
        self.physician_id = physician_id
        self.hospital = None

    def check_in(self, hospital):
        if hospital.register_physician(self.physician_id):
            self.hospital = hospital 
            return True
        return False

    def seek_treatment(self, card):
        # Record visit.
        medical_record = MedicalRecord()
        medical_record.date = time()      
        medical_record.notes = "Patient looks good to me."
        medical_record.signature = self.name
        # Hospital is responsible for adding the new record.
        hospital.write(card, medical_record)          
        
