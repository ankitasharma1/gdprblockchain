from constants import CONFIG_FILE
import yaml

class Parser():
    def __init__(self):
        self.hospitals = dict()
        self.physicians = dict()
        self.physicians_ids = dict()
        self.patients = dict()
        self.patients_ids = dict()
        self.parse()
    
    def parse(self):
        with open(CONFIG_FILE, 'r') as f:
            doc = yaml.load(f)
    
        hospitals = doc['hospitals']    
        physicians = doc['physicians']
        patients = doc['patients']

        # Hospitals.	
        for hospital in hospitals:
            address = hospitals[hospital]['address']
            port = hospitals[hospital]['port']
            self.hospitals.update({hospital: (address, port)}) 

        # Physicians.               
        for physician in physicians:
            address = hospitals[hospital]['address']
            port = hospitals[hospital]['port']
            name = physicians[physician]['name']
            phys_id = physicians[physician]['physician_id']
            self.physicians.update({name: (address, port)})
            self.physicians_ids.update({name: phys_id})

        # Patients.
        for patient in patients:
            address = patients[patient]['address']
            port = patients[patient]['port']
            name = patients[patient]['name']
            patient_id = patients[patient]['patient_id']
            self.patients.update({name: (address, port)})
            self.patients_ids.update({name: patient_id})

    # Hospitals.	
    def get_hosp_names():
        return self.hospitals.keys()

    def valid_hosp(hospital):
        return hospital in self.hospitals

    def get_hosp_contact_info(hospital):
        if hospital in self.hospitals:
            return self.hospitals.get(hospital)
        return None

    # Physicians.               
    def get_phys_names():
        return self.physicians.keys()

    def valid_phys(phys):
        return phys in self.physicians

    def get_phys_contact_info(phys):
        if phys in self.physicians:
            return self.physicians.get(phys)
        return None

    # Patients.
    def get_patient_names():
        return self.patients.keys()

    def valid_patient(patient):
        return patient in self.patients

    def get_patient_contact_info(patient):
        if patient in self.patients:
            return self.patients.get(patient)
        return None
