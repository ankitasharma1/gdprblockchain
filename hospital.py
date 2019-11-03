import crypto
from hasher import hash
from medical_record import MedicalRecord
import csv

class Hospital:
    """
    Hospital is the point of communication for the patient and physician. It is also responsbile for interacting with the public blockchain.
    """
    def __init__(self, name, blockchain):
        """
        Construct a new Hospital object.
        :param name: Hospital name
        :param blockchain: Means to access the blockchain
        """
        self.name = name
        self.blockchain = blockchain
        self.db = dict()
        self.address = None
        self.port = None
        self.staff = []

    """
    API Implementations.
    """

    def register_physician(self, uid):
        """
        Function that registers a physician.
        :param uid: Physician uid
        :return: nothing
        """
        self.staff.append(uid)

    def register_patient(self, name, patient_id):
        """
        Function to register the patient.
        :param name: Patient name
        :param patient_id: Patient id
        :return: card
        """
        uid = name + patient_id
        hash_uid = hash(uid)
        # Check if hashed uid resides on public blockchain.
        if self.blockchain.contains_hash_id(hash_uid):
            print("ERROR: patient affiliated with another hospital")
            return None
        # Generate keys.
        priv_key, pub_key = crypto.generate_keys()
        # Update public blockchain.
        self.add_to_blockchain(hash_uid, pub_key);
        # Populate medical record with patient information.
        medical_record = self.create_first_med_record(name, patient_id)
        # Insert into hospital k,v store.
        self.insert(uid, pub_key, medical_record)
        return Card(uid, priv_key, self.name)

    def write(self, card, medical_record, phy):
        """
        Function to update hospital k,v store with more up to date medical record.
        :param card: Patient card
        :param medical_record: Medical record
        :param phy: Physician
        :return: boolean
        """
        # Validate physician.
        if not self.valid_phy(phy):
            return False
        # Verify that card and hospital name match.
        if not self.valid_card(card):
            return False
        # Obtain the hash index. 
        hash_id = hash(card.uid)
        # Get the public key from the public blockchain.
        block = self.blockchain.get_block(hash_id)
        pub_key = block.pub_key
        # The encrypted uid corresponds to the key in the hospital k,v store.
        hosp_db_key = crypto.encrypt(card.uid, pub_key)
        # Confirm that data belongs to the card holder.
        if self.data_belongs_to_user(hosp_db_key, card):
            # Obtain the most recent medical record for that patient.
            most_recent_write = self.get_last_block(hosp_db_key)
            if most_recent_write:
                # Decrypt the most recent write and convert string to dictionary object
                # for data processing.
                prev = self.deconstruct(crypto.decrypt(most_recent_write, card.priv_key))
                # Merge the prev and current record.
                merged = self.merge(prev, medical_record)
                # Insert the updated medical record into the hospital k,v store.
                self.insert(card.uid, card.priv_key, str(merged))
                return True
            else:
                print("ERROR: Couldn't find block associated with key")
                return False
        else:
            print("ERROR: Private key does not correspond to public key")
            return False
    
    def read(self, uid):
        """
        Function to return all encrypted medical records associated with the patient using their uid.
        :param uid: Patient uid
        :return: encrypted medical records
        """
        # Obtain the hash index. 
        hash_id = hash(uid)
        # Get the public key from the public blockchain.
        block = self.blockchain.get_block(hash_id)
        if block:        
            pub_key = block.pub_key
            # The encrypted uid corresponds to the key in the hospital k,v store.
            hosp_db_key = crypto.encrypt(uid, pub_key)
            blocks = self.get_blocks(hosp_db_key)
            if blocks:            
                return blocks
            else:
                print("ERROR: No data found for patient")
                return None
                    

    def get_staff(self):
        """
        Function to return hospital staff.
        :return: list of hospital staff members.
        """
        return self.staff

    """
    Internal Helper Functions.
    """
            
    def data_belongs_to_user(self, encrypted_db_key, card):
        """
        Function to validate that the encrypted_db_key is indeed the card owner's. The decrypted key should equal the uid using the card's private key.
        :param encrypted_db_key: essentially the encrypted patient uid 
        :param card: patient card that contains the private key
        :return: boolean
        """
        uid = crypto.decrypt(encrypted_db_key, card.priv_key)
        if uid == card.uid:
            return True
        return False

    def valid_card(self, card):
        """
        Function that validates whether the hospital has data for the supplied card.
        :param card: patient card
        :return: boolean
        """
        if card.hospital_name != self.name:
            print("ERROR: invalid request to write")
            return False
        return True

    def merge(self, prev, curr):
        """
        Function that merges the most recent medical record with the current medical record to preserve changes in the past while also keeping track of updates
        :param prev: previous medical record
        :param curr: medical record with update
        :return: merged medical record        
        """
        for k,v in prev.items():
            curr.restore(k,v)
        return curr

    def get_blocks(self, hosp_db_key):
        """
        Function to return all of the data blocks given a hosp_db_key.
        :param hosp_db_key: hospital db key
        :return: list of data blocks
        """
        if hosp_db_key in self.db:
            blocks = self.db.get(hosp_db_key)
            blocks = blocks.split(",")
            return blocks
        return None
    
    def get_last_block(self, hosp_db_key):
        """
        Function to return the most up to date block stored in the hospital k,v store.
        :param hosp_db_key: hospital db key
        :return: block
        """
        if hosp_db_key in self.db:
            blocks = self.db.get(hosp_db_key)
            blocks = blocks.split(",")
            block = blocks[len(blocks) - 1]
            return block
        else:
            return None

    def add_to_blockchain(self, hash_uid, pub_key):
        """
        Function to add block containing hash_uid and pub_key to public blockchain. Adding a block takes two steps, first adding an unconfirmed transaction, and then mining it.
        :param: hash_uid: Hospital hash of the patient uid
        :param: pub_key: Patient public key
        :return: nothing
        """
        self.blockchain.new_transaction(hash_uid, pub_key);
        self.blockchain.mine()

    def create_first_med_record(self, name, patient_id):
        """
        Function to create the very first medical record for a patient.
        :param: name: Patient name
        :param: patient_id: Patient id
        :return: medical record
        """
        med_record = MedicalRecord(self.name)
        med_record.name = name
        med_record.patient_id = patient_id
        med_record.hospital = self.name
        med_record.notes = ""
        return med_record

    def valid_phy(self, phy):
        """
        Function to validate that physician has registered with hospital.
        :param: phy: physician
        :return: boolean
        """
        if phy in self.staff:
            return True
        print("ERROR: physician not a registered staff member")
        return False

    def deconstruct(self, med_record):
        """
        Function to transform string representation of medical record into a dictionary.
        :param: med_record: medical record
        :return: dictionary
        """
        # Refer to string representation of the medical record to understand this parsing.
        med_record = med_record.split(",")
        n = dict()        
        for m in med_record:
            temp = m
            m = m.split(":")
            # TODO:Edge case, clean up later. A more readable time data point contains a : which is what we are delimiting the rest of the data by.
            if m[0] == "date":
                m[1] = temp.replace("date:", "")
            n.update({m[0]: m[1]})
        return(n)
            
    def insert(self, uid, public_key, medical_record):
        """
        Function to insert encrypted medical record into hospital k,v store.
        :param: uid: Patient uid
        :param: public_key: Patient public key
        :param: medical_record: Medical record
        :return: nothing
        """
        key = crypto.encrypt(uid, public_key)
        value = crypto.encrypt(str(medical_record), public_key)
        if key in self.db.keys():
            value = self.db.get(key) + "," + value
        self.db.update({key: value})         

class Card:
    """
    Card created by the hospital.
    """
    def __init__(self, uid, priv_key, name):
        """
        Construct a new Card object.
        :param uid: Patient uid
        :param priv_key: Patient private key
        :param name: Patient name
        """
        self.uid = uid
        self.priv_key = priv_key
        self.hospital_name = name

    def update(self, hospital_name):
        """
        Construct a new Card object.
        :param hospital_name: Hospital name
        :return: nothing
        """
        self.hospital_name = hospital_name

