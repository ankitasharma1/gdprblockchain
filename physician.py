from medical_record import MedicalRecord
import time
import crypto
import phys_msg
import socket
from constants import ERROR
from constants import MESSAGE_SIZE
import constants
import card_helper
import patient_msg

class Physician():
    """
    Physician interacts with patients and forwards writes to the hospital.
    """
    def __init__(self, name, physician_id):
        """
        Construct a new Physician object.
        :param name: Physician name
        :param physician_id: Physician id
        """
        self.name = name
        self.physician_id = physician_id
        self.hospitals = []

    def send_msg(self, msg, address, port):
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

    def send_msg_get_socket(self, msg, address, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((address, port))
            s.send(msg)
            return s
        except Exception, e:
            print(e)
            print("Unable to connect")
            s.close()
            return ERROR
            
        s.close()
        return 0

    def register(self, hospital_name, hospital_address, hospital_port):
        """
        Register with a hospital.
        :param hospital_address: Hospital address
        :param hospital_port: Hospital port
        :return: nothing
        """
        response = self.send_msg(phys_msg.register_msg(self.name, self.physician_id), hospital_address, hospital_port)
        if isinstance(response , int):
            print("ERROR: Hospital server error")
            return
        if response.get(constants.TYPE) != phys_msg.REGISTER_RESPONSE:
            print("ERROR: incorrect response type from hospital, should have received %s" %(phys_msg.REGISTER_RESPONSE))
            return

        # Hospital returns a boolean.
        if response.get(phys_msg.RESPONSE):
            self.hospitals.append(hospital_name)
            print("%s registered with %s" %(self.name, hospital_name))
            return True
        else:
            print("Unable to register with hospital.")
            return False

    def seek_treatment(self, card_path, hospital_address, hospital_port):
        """
        Function to handle patient request and to write to hospital db k,v store.
        :param card_path: Patient card
        :param hospital_address: Hospital address
        :param hospital_port: Hospital port
        :return: boolean
        """
        card = card_helper.get_card_object(card_path)
        medical_record = MedicalRecord(self.name, card)
        medical_record.notes = "Patient looks good to me."
        response = self.send_msg(phys_msg.write_msg(card_path, str(medical_record), self.physician_id), hospital_address, hospital_port)
        if isinstance(response , int):
            print("ERROR: Hospital server error")
            return
        if response.get(constants.TYPE) != phys_msg.WRITE_RESPONSE:
            print("ERROR: incorrect response type from hospital, should have received %s" %(phys_msg.WRITE_RESPONSE))
            return

        # Hospital returns a boolean.
        if response.get(phys_msg.RESPONSE) :
            print("Successfully wrote to hospital db")
            return True
        else:
            print("Write was not successful")  
            return False       

    def read_patient_record(self, card_path, hospital_address, hospital_port):
        """
        Function to handle patient issuing request for physician to read their medical data.
        :param card_path: Patient card
        :param hospital_address: Hospital address
        :param hospital_port: Hospital port
        :return: boolean
        """
        card = card_helper.get_card_object(card_path)
        if card == None:
            return False
                
        if not self.hospital_affiliation_valid(card.hospital_name):
            print("ERROR: " + self.name + " is not registered with hospital")
            return False      

        # Copied patient code.
        socket = self.send_msg_get_socket(patient_msg.read_msg(card.uid), hospital_address, hospital_port)
        if isinstance(socket, int):
            return
        data = socket.recv(MESSAGE_SIZE)
        if data:
            responses = constants.deserialize(data)
            for response in responses:
                if isinstance(response , int):
                    socket.close()
                    return
                if response.get(patient_msg.RESPONSE):
                    print(crypto.decrypt(response.get(patient_msg.BLOCK), card.priv_key))                
                    num_blocks = response.get(patient_msg.NUM_BLOCKS)
                    # Special casing the first response before reading the rest.
                    for i in range(1, num_blocks):
                        data = socket.recv(MESSAGE_SIZE)
                        if data:
                            responses = constants.deserialize(data)
                            for response in responses: 
       		                    print(crypto.decrypt(response.get(patient_msg.BLOCK), card.priv_key))
            
                else:
                    print("No records were retrieved.")
                    socket.close()
                    return False
        socket.close()
        return True

    def transfer_patient_record(self, card, src_hospital, dst_hospital):
        """
        Function to handle patient issuing request for physician to transfer their medical data.
        :param card: Patient card
        :param src_hospital: Where data is currently stored.
        :param dst_hospital: Where data is requested to be transferred.
        :return: boolean
        """
        if not self.hospital_affiliation_valid(src_hospital):
            print("ERROR: " + self.name + " is not registered with hospital")
            return False            
        if src_hospital.transfer(card, dst_hospital):
            return True        

    def hospital_affiliation_valid(self, hospital_name):
        """
        Function to validate that physician is registered with the hospital.
        :param: hospital_name: Hospital name
        :return: boolean
        """
        if hospital_name in self.hospitals:
            return True
        print("ERROR: " + self.name + " is not affiliated with " + hospital.name)
        return False

    def get_hospitals(self):
        return self.hospitals
