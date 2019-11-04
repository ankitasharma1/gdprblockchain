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
    print("---------> Test Registration")
    assert(pa1.register(h1) == True)
    # Simulate patient "losing" card and registering with another hospital.
    print("---------> Double Registration")
    pa1.card = None
    assert(pa1.register(h2) == False)
    # Test registration, write, and read.
    print("---------> Test Registration/Write/Read")    
    assert(pa2.register(h1) == True)
    ph1.register(h1)
    # TODO: hospital can be resolved from the card.
    pa2.seek_treatment(ph1, h1)
    pa2.read(h1)
    print("---------> Read from another hospital that does not store our data")
    # Try reading from a hospital that does not contain our data.
    pa2.read(h2)
    print("---------> Test that physician can read patient's records")
    # Test that physician can read medical records for patient.
    pa2.read_medical_record(ph1, h1)
    print("---------> Remove patient data")
    # Remove patient data.
    assert(pa2.remove(h1) == True)
    print("---------> Read removed data")
    # Try to read data.
    pa2.read(h1)    
    print("---------> Test patient request to transfer")
    ph3.register(h1)
    pa2.seek_treatment(ph3, h1)
    pa2.read(h1)
    assert(pa2.transfer(h1, h3) == True)
    pa2.read(h3)
    ph2.register(h3)
    print("---------> Add data to new hospital and return")
    pa2.seek_treatment(ph2, h3)
    pa2.read(h3)
    print("---------> Test physician request to transfer")
    pa2.transfter_medical_record(ph1, h3, h2)    
def main():
    parse(CONFIG_FILE)

main()
