import socket
from threading import Thread
import crypto

NAME = "name"
PATIENT_ID = "patient_id"
HOSPITAL = "hospital"

class Patient:
    """
    Patient can issue requests to the hospital and physicians.
    """
    def __init__(self, name, patient_id):
        """
        Construct a new Patient object.
        :param name: Patient name
        :param patient_id: Patient id
        """
        self.name = name
        self.patient_id = patient_id
        self.card = None

    def register(self, hospital): 
        """
        Function to register with a hospital.
        :param hospital: Hospital
        :return: boolean
        """       
        if self.card == None:
            self.card = hospital.register_patient(self.name, self.patient_id)
            if self.card:
                return True
            else:
                return False 

    def seek_treatment(self, physician, hospital):
        """
        Function for a patient to seek treatment from a physician.
        :param physician: Physician
        :param hospital: Hospital TODO: This will not be needed later.
        :return: nothing
        """       
        physician.seek_treatment(self.card, hospital)

    def read(self, hospital):
        """
        Function for a patient to read all of their data.
        :param hospital: Hospital
        :return: nothing
        """       
        if self.card:
            records = hospital.read(self.card.uid)
        if records:
		    for record in records:
		        record = crypto.decrypt(record, self.card.priv_key)
		        print(record)               

    def read_medical_record(self, physician, hospital):
        """
        Function for a patient to give a physician permission to read their data.
        :param physician: Physician
        :param hospital: Hospital
        :return: nothing
        """       
        if self.card:
            physician.read_patient_record(self.card, hospital)


    def remove(self, hospital):
        """
        Function for a patient to remove all of their data.
        :param hospital: Hospital
        :return: boolean
        """       
        if self.card:
            if hospital.remove(self.card):
                 return True
        return False

    def transfer(self, src_hospital, dst_hospital):
        """
        Function to transfer data to another hospital
        :param src_hospital: Current hospital
        :param dst_hospital: New hospital
        :return: boolean
        """       
        if self.card:
            if src_hospital.transfer(self.card, dst_hospital):
                 return True
        return False

