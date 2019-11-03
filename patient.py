import socket
from threading import Thread

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

    def check_in(self, hospital):        
        if self.card == None:
            self.card = hospital.register_patient(self.name, self.patient_id)
            if self.card:
                return True
            else:
                return False 

    def seek_treatment(self, physician):
        physician.seek_treatment(self.card)
               
        

