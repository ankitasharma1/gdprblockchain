from medical_record import MedicalRecord
import time
import crypto

class Physician():
    """
    Physician interacts with patients and forwards writes to the hospital.
    """
    def __init__(self, name, physician_id):
        """
        Construct a new Physician object.
        :param name: Physician name
        :param physician_id: Physician id
        """
        self.name = name
        self.physician_id = physician_id
        self.hospitals = []

    def register(self, hospital):
        """
        Register with a hospital.
        :param hospita: hospital
        :return: nothing
        """
        hospital.register_physician(self.physician_id)
        self.hospitals.append(hospital.name)

    def seek_treatment(self, card, hospital):
        """
        Function to handle patient request and to write to hospital db k,v store.
        :param card: Patient card
        :param hospital: Hospital TODO: This will not be needed later.
        :return: nothing
        """
        medical_record = MedicalRecord(self.name)
        medical_record.notes = "Patient looks good to me."
        hospital.write(card, medical_record, self.physician_id)          

    def read_patient_record(self, card, hospital):
        """
        Function to handle patient issuing request for physician to read their medical data.
        :param card: Patient card
        :param hospital: Hospital TODO: This will not be needed later.
        :return: nothing
        """
        if not self.hospital_affiliation_valid(hospital):
            print("ERROR: physician not registered with hospital")
            return False            
        records = hospital.read(card.uid)
        if records:
		    for record in records:
		        record = crypto.decrypt(record, card.priv_key)
		        print(record)               
 
    def hospital_affiliation_valid(self, hospital):
        """
        Function to validate that physician is registered with the hospital.
        :param: hospital: Hospital
        :return: boolean
        """
        if hospital.name in self.hospitals:
            return True
        return False
