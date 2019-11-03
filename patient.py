import socket
from threading import Thread
import crypto

NAME = "name"
PATIENT_ID = "patient_id"
HOSPITAL = "hospital"

class Patient:
    def __init__(self, name, patient_id):
        self.name = name
        self.patient_id = patient_id
        # TODO: Stretch Goal - keep track of their own records.
        self.record_path = None
        self.card = None

    def register(self, hospital):        
        if self.card == None:
            self.card = hospital.register_patient(self.name, self.patient_id)
            if self.card:
                return True
            else:
                return False 

    def seek_treatment(self, physician, hospital):
        physician.seek_treatment(self.card, hospital)

    def read(self, hospital):
        if self.card:
            records = hospital.read(self.card.uid)
        if records:
		    for record in records:
		        record = crypto.decrypt(record, self.card.priv_key)
		        print(record)               

    def read_medical_record(self, physician, hospital):
        if self.card:
            physician.read_patient_record(self.card, hospital)
        

