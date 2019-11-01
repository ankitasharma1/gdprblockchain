import yaml
import subprocess
from blockchain import Blockchain
from hospital import Hospital
from hasher import Hasher
from patient import Patient

CONFIG_FILE = 'config.yaml'

def parse(path):
    # Create the blockchain.
    blockchain = Blockchain()

    # create the hasher
    hasher = Hasher()

    with open(path, 'r') as f:
        doc = yaml.load(f)

    hospitals = doc['hospitals']    
    hospital_dbs = doc['hospital_dbs']
    patients = doc['patients']

    process = subprocess.Popen(
        "sudo gnome-terminal -x python f.py", 
        stdout=subprocess.PIPE,
        stderr=None,
        shell=True
    )

    for db, hospital in zip(hospital_dbs, hospitals):
        f = open(hospital_dbs[db]['path'], 'w+')
        h = Hospital(blockchain, hasher,f)
        h.set_address(hospitals[hospital]['address'])
        h.set_port(hospitals[hospital]['port'])
        h.handle_connection()
        #os.system("gnome-terminal -e 'bash -c \"sudo apt-get update; exec bash\"'")

    for patient in patients:
        p = Patient(patients[patient]['name'], patients[patient]['gov_id'])
        p.set_address(patients[patient]['address'])
        p.set_port(patients[patient]['address'])
        p.handle_connection()

def main():
    parse(CONFIG_FILE)

main()