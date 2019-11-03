import yaml
from blockchain import Blockchain
from hospital import Hospital
from patient import Patient
from physician import Physician

# File which contains information for the world we are simulating.
CONFIG_FILE = 'config.yaml'

def parse(path):
    """
    Function to parse the config file and to create all of the objects.
    :param path: path to config file    
    """
    # Create the blockchain.
    blockchain = Blockchain()

    with open(path, 'r') as f:
        doc = yaml.load(f)

    hospitals = doc['hospitals']    
    physicians = doc['physicians']
    patients = doc['patients']

    # Hospitals.	
    h = []
    for hospital in hospitals:
        address = hospitals[hospital]['address']
        port = hospitals[hospital]['port']
        h.append(Hospital(hospital, blockchain))

    # Physicians.
    ph = []
    for physician in physicians:
        address = hospitals[hospital]['address']
        port = hospitals[hospital]['port']
        name = physicians[physician]['name']
        phys_id = physicians[physician]['physician_id']
        ph.append(Physician(name, phys_id))
    
    # Patients.
    pa = []
    for patient in patients:
        address = patients[patient]['address']
        port = patients[patient]['port']
        pa.append(Patient(patients[patient]['name'], patients[patient]['patient_id']))

    simulate(h, ph, pa)

"""
Helper function to simulate interactions.
"""
def simulate(hospitals, physicians, patients):
    h1 = hospitals[0]
    h2 = hospitals[1]
    h3 = hospitals[2]
        
    ph1 = physicians[0]
    ph2 = physicians[1]
    ph3 = physicians[2]

    pa1 = patients[0]
    pa2 = patients[1]
    pa3 = patients[2]

    # Test registration.
    assert(pa1.register(h1) == True)
    # Simulate patient "losing" card and registering with another hospital.
    pa1.card = None
    assert(pa1.register(h2) == False)

    # Test registration, write, and read.    
    assert(pa2.register(h1) == True)
    ph1.register(h1)
    # TODO: hospital can be resolved from the card.
    pa2.seek_treatment(ph1, h1)
    pa2.read(h1)
    pa2.read(h2)
    pa2.read_medical_record(ph1, h1)
        
def main():
    parse(CONFIG_FILE)

main()
