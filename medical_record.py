import json
import time

NAME = "name"
PATIENT_ID = "patient_id"
HOSPITAL = "hospital"
DATE = "date"
NOTES = "notes"
SIGNATURE = "signature"

class MedicalRecord:
    def __init__(self, name):
        self.name = None
        self.patient_id = None
        self.hospital = None
        self.date = time.ctime()
        self.notes = None
        self.signature = name
    
    def restore(self, k, v):
        if k == NAME:
            if self.name == None:
                self.name = v
        elif k == PATIENT_ID:
            if self.patient_id == None:
                self.patient_id = v
        elif k == HOSPITAL:
            if self.hospital == None:
                self.hospital = v
        elif k == DATE:
            if self.date == None:
                self.date = v
        elif k == NOTES:
            if self.notes == None:
                self.notes = v
        elif k == SIGNATURE:
            if self.signature == None:
                self.signature = v
        else:
            print(k)    
            print("ERROR: unexpected type")

    def __str__(self):
        name = str(self.name)
        patient_id = str(self.patient_id)
        hospital = str(self.hospital)
        date = str(self.date)
        notes = str(self.notes)
        signature = str(self.signature)
        result = NAME + ":" + name + "," + PATIENT_ID + ":" + patient_id + "," + HOSPITAL + ":" + hospital + "," + DATE + ":" + date + "," + NOTES + ":" + notes + "," + SIGNATURE + ":" + signature
        return result
