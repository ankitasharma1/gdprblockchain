import json
import time

NAME = "name"
PATIENT_ID = "patient_id"
HOSPITAL = "hospital"
DATE = "date"
NOTES = "notes"
SIGNATURE = "signature"

class MedicalRecord:
    """
    Standardized medical record format.
    """
    def __init__(self, name, card=None):
        """
        Construct a new MedicalRecord object.
        :param card: Patient card to help populate the basic medical record.
        :param name: Name of entity that is creating the medical record.
        """
        if card:
            self.name = card.patient_name
            self.patient_id = card.patient_id
            self.hospital = card.hospital_name
        else:
            self.name = None
            self.patient_id = None
            self.hospital = None

        # Default set.        
        self.date = time.ctime()
        self.notes = None
        self.signature = name
    
    def restore(self, k, v):
        """
        Before restoring the current medical record with previous information, check that the current medical record does not have this information.
        :param k: Key
        :param v: Value
        """
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
