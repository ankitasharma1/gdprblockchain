import crypto
from hasher import hash
from medical_record import MedicalRecord
from time import time

class Hospital:
    def __init__(self, name, blockchain, db, staff):
        self.name = name
        self.blockchain = blockchain
        self.db = db
        self.address = None
        self.port = None
        self.staff = staff

    def register_physician(self, uid):
        if uid in self.staff:
            return True
        print("ERROR: physician not a registered staff member")
        return False

    def register_patient(self, name, patient_id):
        uid = name + patient_id
        hash_uid = hash(uid)
        if self.blockchain.contains_hash_id(hash_uid):
            print("ERROR: patient affiliated with another hospital")
            return None
        priv_key, pub_key = crypto.generate_keys()
	self.add_to_blockchain(hash_uid, pub_key);
        self.create_first_med_record(name, patient_id)
	return Card(uid, priv_key, self.name)

    def add_to_blockchain(self, hash_uid, pub_key):
	self.blockchain.new_transaction(hash_uid, pub_key);
	self.blockchain.mine()

    def create_first_med_record(self, name, patient_id):
        med_record = MedicalRecord()
        med_record.name = name
        med_record.patient_id = patient_id
        med_record.hospital = self.name
        med_record.date = time()
        med_record.notes = ""
        med_record.signature = self.name
        return med_record

    def clean_up(self):
        self.db.close()

class Card:
    def __init__(self, uid, priv_key, name):
        self.uid = uid
        self.priv_key = priv_key
        self.hospital_name = name

    def update(self, hospital_id):
        self.hospital_id = hospital_id

