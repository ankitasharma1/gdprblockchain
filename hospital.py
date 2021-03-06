import crypto
from hasher import hash
from medical_record import MedicalRecord
import socket
import bc_msg
from constants import ERROR
from Crypto.PublicKey import RSA
import time
import hospital_msg
from constants import MESSAGE_SIZE
import constants

class Hospital:
    """
    Hospital is the point of communication for the patient and physician. It is also responsbile for interacting with the public blockchain.
    """
    def __init__(self, name, bc_address, bc_port):
        """
        Construct a new Hospital object.
        :param: name: Hospital name
        :param: bc_address: Blockchain proxy server address
        :param: bc_port: Blockchain proxy server port
        """
        self.name = name
        self.bc_address = bc_address
        self.bc_port = int(bc_port)
        self.db = dict()
        self.staff = []
        self.staff_names = []

    """
    API Implementations.
    """
    def send_message_to_bc(self, msg, pub_key=None):
        """
        Helper function that sends a message to the blockchain server.
        :param: msg: Message to send
        :param: pub_key: Public key RSA object that may be sent with the message
        :return: response to message
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.bc_address, self.bc_port))
            #print("Connected to %s:%s" %(self.bc_address, self.bc_port))
            s.send(msg)
            # Send public key if bc is expecting it.
            if bc_msg.bc_expecting_pub_key(bc_msg.deserialize(msg)):
                if pub_key:
                    s.send(pub_key.exportKey(format='PEM', passphrase=None, pkcs=1))
                else:
                    print("ERROR: BC expecting public key")            
            # Check to see if message requires a response.
            if bc_msg.requires_response(bc_msg.deserialize(msg)):
                # Check if we are receiving a pub key.                       
                if bc_msg.hosp_expecting_pub_key(bc_msg.deserialize(msg)):
                    return RSA.importKey(s.recv(1024), passphrase=None)
                # Receiving a normal json response.                        
                data = s.recv(bc_msg.MESSAGE_SIZE)  
                if data:
                    messages = bc_msg.deserialize(data)
                    for message in messages:
                        s.close()
                        return message.get(bc_msg.RESPONSE)
        except Exception, e:
            print(e)
            #print("ERROR: unable to send request %s to blockchain server" %(msg))
            s.close()
            return ERROR
            
        s.close()
        return 0

    def send_msg(self, msg, address, port):
        """
        Helper function to send a message to the given address.
        :param: msg: Message to send
        :param: address: Address to send to
        :param: port: Port client is listening on
        :return: response to message
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((address, port))
            # Send a message.
            s.send(msg)
            # Wait to receive response.
            data = s.recv(MESSAGE_SIZE)
            if data:
                messages = constants.deserialize(data)
                for message in messages:
                    s.close()
                    return message
        except Exception, e:
            print(e)
            #print("ERROR: unable to send request %s" %(msg))
            s.close()
            return ERROR
            
        s.close()
        return 0

    def register_physician(self, name, uid):
        """
        Function that registers a physician.
        :param: name: Physician name
        :param uid: Physician uid
        :return: boolean
        """
        if uid not in self.staff:
            self.staff_names.append(name)
            self.staff.append(uid)
            return True
        print("ERROR: physician with that UID has already registered.")
        return False

    def register_patient(self, patient_name, patient_id):
        """
        Function to register the patient.
        :param patient_name: Patient name
        :param patient_id: Patient id
        :return: card
        """
        uid = patient_name + patient_id
        hash_uid = hash(uid)
        # Check if hashed uid resides on public blockchain.
        print(">>> Sending request to bc to check if %s exists in blockchain" %(hash_uid))
        response = self.send_message_to_bc(bc_msg.contains_hash_uid_msg(hash_uid))
        if response == ERROR:
            return None
        if response:
            print("ERROR: Patient " + patient_name + " is affiliated with a hospital already")
            return None
        # Generate keys.
        priv_key, pub_key = crypto.generate_keys()
        # Update public blockchain.
        self.add_to_blockchain(hash_uid, pub_key);
        card = Card(patient_name, patient_id, uid, priv_key, self.name)
        # Insert into hospital k,v store.
        self.insert(uid, pub_key, MedicalRecord(self.name, card))
        return card

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
        hash_uid = hash(card.uid)
        # Get the public key from the public blockchain.
        print(">>> Sending request to get pub_key for write request")
        pub_key = self.send_message_to_bc(bc_msg.get_pub_key(hash_uid))
        if not pub_key:
            return False
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
            else:
                self.insert(card.uid, card.priv_key, str(medical_record))
            return True
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
        hash_uid = hash(uid)
        # Get the public key from the public blockchain.
        print(">>> Sending request to get pub_key for read request")
        pub_key = self.send_message_to_bc(bc_msg.get_pub_key(hash_uid))
        if pub_key:        
            # The encrypted uid corresponds to the key in the hospital k,v store.
            hosp_db_key = crypto.encrypt(uid, pub_key)
            blocks = self.get_blocks(hosp_db_key)
            if blocks:            
                return blocks
            else:
                print("ERROR: No data found for patient")
                return None

    def remove(self, card):
        """
        Function to remove all patient data.
        :param card: card
        :return: boolean
        """
        # Verify that card and hospital name match.
        if not self.valid_card(card):
            return False
        # Obtain the hash index. 
        hash_uid = hash(card.uid)
        # Get the public key from the public blockchain.
        print(">>> Sending request to get pub_key for remove request")
        pub_key = self.send_message_to_bc(bc_msg.get_pub_key(hash_uid))
        # The encrypted uid corresponds to the key in the hospital k,v store.
        hosp_db_key = crypto.encrypt(card.uid, pub_key)
        # Confirm that data belongs to the card holder.
        if self.data_belongs_to_user(hosp_db_key, card):
            self.db.pop(hosp_db_key)
            return True
        else:
            print("ERROR: Private key does not correspond to public key")
            return False                 

    def transfer(self, card, card_path, dst_hospital_name, dst_hospital_address, dst_hospital_port):
        """
        Function to transfer patient data to another hospital.
        :param card: card
        :param card_path: card path
        :param dst_hospital_name: name of hospital where records are being transferred to
        :param dst_hospital_address: hospital address to transfer data to
        :param dst_hospital_port: hospital port
        :return: boolean
        """

        # Verify that card and hospital name match.
        if not self.valid_card(card):
            print("ERROR: invalid card, unable to accomodate transfer request")
            return False
        # Obtain the hash index. 
        hash_uid = hash(card.uid)
        # Get the public key from the public blockchain.
        print(">>> Sending request to get pub_key for read request")
        pub_key = self.send_message_to_bc(bc_msg.get_pub_key(hash_uid))
        # The encrypted uid corresponds to the key in the hospital k,v store.
        hosp_db_key = crypto.encrypt(card.uid, pub_key)
        # Confirm that data belongs to the card holder.
        if self.data_belongs_to_user(hosp_db_key, card):
            # Check if other hospital is able to transfer the records
            if self.db.get(hosp_db_key):
                blocks = self.db.get(hosp_db_key).split(",")
                for block in blocks:
                    response = self.send_msg(hospital_msg.transfer_write_msg(hosp_db_key, block), dst_hospital_address, dst_hospital_port)         
                    #if dst_hospital.transfer_write(hosp_db_key, self.db.get(hosp_db_key)):
                    if isinstance(response , int):
                        print("Hospital server error")
                        return False
                    if not response.get(hospital_msg.RESPONSE):                
                        return False
            
                # Remove data from this hospital.
                self.db.pop(hosp_db_key)
            # Even if there may be no data to transfer, update the card.
            # Update hospital name on patient card.
            card.update(dst_hospital_name)
            # Update card to store the location of where the private key is stored.
            card.priv_key = card.priv_key_path
            f = open(card_path, "w+")
            f.write(str(card))
            f.close()
            print("Successfully transferred records to %s" %(card.hospital_name))
            return True
        else:
            print("ERROR: No data found for patient")
            return False

    def transfer_write(self, hosp_db_key, block):
        """
        Function to transfer encrypted medical records to our db.
        :param hosp_db_key: hospital db key
        :param blocks: encrypted medical records
        :return: boolean
        """

        if hosp_db_key in self.db.keys():
            value = self.db.get(hosp_db_key) + "," + block
            self.db.update({hosp_db_key: value})         
        else:
            self.db.update({hosp_db_key: block})

        return True

    def get_staff(self):
        """
        Function to return hospital staff.
        :return: list of hospital staff members.
        """
        return self.staff_names

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
        if card:
            if card.hospital_name != self.name:
                return False
            return True
        print("ERROR: no card provided")
        return False

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
        print(">>> Sending request to bc to add new txn")
        self.send_message_to_bc(bc_msg.new_txn(hash_uid, ""), pub_key)
        # Adding a new transaction implicitly means to mine it.
        # print(">>> Sending request to bc to mine the new txn")
        # self.send_message_to_bc(bc_msg.mine()) 

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

    def get_db(self):
        """
        Function to return hospital db.
        :return: hospital db
        """
        return self.db

class Card:
    """
    Card created by the hospital.
    """
    def __init__(self, patient_name, patient_id, uid, priv_key, hospital_name):
        """
        Construct a new Card object.
        :param patient_name: Name of the patient
        :param patient_id: Id of the patient
        :param uid: Patient uid
        :param priv_key: Patient private key
        :param hospital_name: Name of the hospital
        """
        self.patient_name = patient_name
        self.patient_id = patient_id
        self.uid = uid
        self.priv_key = priv_key
        self.hospital_name = hospital_name
        self.priv_key_path = None

    def update(self, hospital_name):
        """
        Update param of card.
        :param hospital_name: Hospital name
        :return: nothing
        """
        self.hospital_name = hospital_name

    def __str__(self):
        card_to_string = ""
        card_to_string = card_to_string + str(self.patient_name) + ","
        card_to_string = card_to_string + str(self.patient_id) + ","
        card_to_string = card_to_string + str(self.uid) + ","
        card_to_string = card_to_string + str(self.priv_key) + ","
        card_to_string = card_to_string + str(self.hospital_name)
        return card_to_string
