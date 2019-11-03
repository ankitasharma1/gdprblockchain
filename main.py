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
    files = []
    for hospital in hospitals:
        address = hospitals[hospital]['address']
        port = hospitals[hospital]['port']
        path = hospitals[hospital]['db_path']
        files.append(path)
        f = open(path, 'w+')
        staff = hospitals[hospital]['staff']
        h.append(Hospital(hospital, blockchain, f, staff))

    ph = []
    for physician in physicians:
        address = hospitals[hospital]['address']
        port = hospitals[hospital]['port']
        ph.append(Physician(physicians[physician]['name'], physicians[physician]['physician_id']))

    pa = []
    for patient in patients:
        address = patients[patient]['address']
        port = patients[patient]['port']
        pa.append(Patient(patients[patient]['name'], patients[patient]['patient_id']))

    simulate(h, ph, pa)
    clean_up(files)

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
    # Test double registration.
    assert(pa1.check_in(h1) == True)
    pa1.card = None
    assert(pa1.check_in(h2) == False)
    """
    
    #assert(pa1.check_in(h1) == True)
	#assert(ph1.check_in(p1) == True)
    #pa1.seek_treatment(ph1)

def clean_up(files):
    for file in files:
        os.unlink(file)

def main():
    parse(CONFIG_FILE)

main()
