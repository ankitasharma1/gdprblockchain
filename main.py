import yaml
import subprocess
from blockchain import Blockchain
from hospital import Hospital
from patient import Patient
from physician import Physician
import os
from threading import Thread
import signal
import sys
from subprocess import Popen, PIPE
import shutil

CONFIG_FILE = 'config.yaml'

def parse(path):
    # Create the blockchain.
    blockchain = Blockchain()

    with open(path, 'r') as f:
        doc = yaml.load(f)

    hospitals = doc['hospitals']    
    physicians = doc['physicians']
    patients = doc['patients']
	
    h = []
    for hospital in hospitals:
        address = hospitals[hospital]['address']
        port = hospitals[hospital]['port']
        staff = hospitals[hospital]['staff']
        h.append(Hospital(hospital, blockchain, staff))

    ph = []
    for physician in physicians:
        address = hospitals[hospital]['address']
        port = hospitals[hospital]['port']
        name = physicians[physician]['name']
        phys_id = physicians[physician]['physician_id']
        ph.append(Physician(name, phys_id))

    pa = []
    for patient in patients:
        address = patients[patient]['address']
        port = patients[patient]['port']
        pa.append(Patient(patients[patient]['name'], patients[patient]['patient_id']))

    simulate(h, ph, pa)

def simulate(hospitals, physicians, patients):
    h1 = hospitals[0]
    h2 = hospitals[1]
    h3 = hospitals[2]

    # Sort, problems with parsing order.
    sorted_physicians = sorted(physicians, key=lambda x: x.physician_id)
        
    ph1 = sorted_physicians[0]
    ph2 = sorted_physicians[1]
    ph3 = sorted_physicians[2]

    pa1 = patients[0]
    pa2 = patients[1]
    pa3 = patients[2]

    """
    # Test double registration.
    assert(pa1.check_in(h1) == True)
    pa1.card = None
    assert(pa1.check_in(h2) == False)
    """
    
    assert(pa1.check_in(h1) == True)
    assert(ph1.check_in(h1) == True)
    pa1.seek_treatment(ph1)
    pa1.read(h1)
    
def main():
    parse(CONFIG_FILE)

main()
