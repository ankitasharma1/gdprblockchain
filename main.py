import yaml
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

    hospital_list = []

    for db, hospital in zip(hospital_dbs, hospitals):
        f = open(hospital_dbs[db]['path'], 'w+')
        h = Hospital(blockchain, hasher,f)
        hospital_list.append(h)

    patient_list = []

    for patient in patients:
        p = Patient(patients[patient]['name'], patients[patient]['gov_id'])
        patient_list.append(p)

    ## Clean up ##
    for h in hospital_list:
        h.db.close()

def main():
    parse(CONFIG_FILE)

main()