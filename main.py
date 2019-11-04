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
    #blockchain = Blockchain()

    with open(path, 'r') as f:
        doc = yaml.load(f)

    bc_proxy_server = doc['bc_proxy_server']    
    hospitals = doc['hospitals']    
    physicians = doc['physicians']
    patients = doc['patients']

    # BC Proxy Server.
    bc_address = bc_proxy_server['address']
    bc_port = bc_proxy_server['port']
	
    # Hospitals.	
    h = []
    for hospital in hospitals:
        address = hospitals[hospital]['address']
        port = hospitals[hospital]['port']
        h.append(Hospital(hospital, bc_address, bc_port))

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

    connect(h, ph, pa)
    #simulate(h, ph, pa)

def connect(hospitals, physicians, patients):
    h1 = hospitals[0]
    h2 = hospitals[1]
    h3 = hospitals[2]
        
    ph1 = physicians[0]
    ph2 = physicians[1]
    ph3 = physicians[2]

    pa1 = patients[0]
    pa2 = patients[1]
    pa3 = patients[2]

    h1.send_pub_key()

    #assert(pa1.register(h1) == True)

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

    """
    >>>> Tests <<<<
    """

    test_reg(pa1, h1)
    test_patient_losing_card(pa1, h2)
    test_reg_wr_rd(pa2, ph1, h1)
    test_rd_from_another_hospital(pa2, h2)

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
    assert(pa2.transfer_medical_record(h3, h2, ph2) == True) 
    pa2.read(h2) 

# Test patient registration
def test_reg(pa, h):
    print("---------> Test Registration")
    assert(pa.register(h) == True)

# Simulate patient "losing" card and registering with another hospital.
def test_patient_losing_card(pa, h):
    print("---------> Double Registration")
    pa.card = None
    assert(pa.register(h) == False)    

# Test registration, write, and read.
def test_reg_wr_rd(pa, ph, h):
    print("---------> Test Registration/Write/Read")    
    assert(pa.register(h) == True)
    ph.register(h)
    # TODO: hospital can be resolved from the card.
    pa.seek_treatment(ph, h)
    pa.read(h)

# Try reading from a hospital that does not contain our data.
def test_rd_from_another_hospital(pa, h):
    print("---------> Read from another hospital that does not store our data")
    pa.read(h)
  
def main():
    parse(CONFIG_FILE)

main()
