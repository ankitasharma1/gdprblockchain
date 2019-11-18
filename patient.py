import socket
from threading import Thread
import crypto
import patient_msg
import card_helper
from constants import ERROR
from constants import MESSAGE_SIZE
import constants

NAME = "name"
PATIENT_ID = "patient_id"
HOSPITAL = "hospital"

class Patient:
    """
    Patient can issue requests to the hospital and physicians.
    """
    def __init__(self, name, patient_id):
        """
        Construct a new Patient object.
        :param name: Patient name
        :param patient_id: Patient id
        """
        self.name = name
        self.patient_id = patient_id
        self.card_path = None
        self.card = None

    def set_card_path(self, path):
        self.card_path = path

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

    def register(self, hospital_address, hospital_port): 
        """
        Function to register with a hospital.
        :param hospital_address: Hospital address
        :param hospital_port: Hospital port
        :return: boolean
        """       
        response = self.send_msg(patient_msg.register_msg(self.name, self.patient_id), hospital_address, hospital_port)
        if isinstance(response , int):
            print("ERROR: Hospital server error")
            return

        # Check if appropriate response is received.
        if response.get(constants.TYPE) != patient_msg.REGISTER_RESPONSE:
            print("ERROR: incorrect response type from hospital, should have received %s" %(patient_msg.REGISTER_RESPONSE))
            return

        # Hospital returns a boolean.
        if response.get(patient_msg.RESPONSE):
            print("Obtained card from hospital.")
            self.card = card_helper.get_card_object(self.card_path)
            return True
        else:
            print("Unable to register with hospital.")
            return False

    def seek_treatment(self, physician_address, physician_port):
        """
        Function for a patient to seek treatment from a physician.
        :param physician_address: Physician address
        :param physician_port: Physician port
        :return: nothing
        """
        if self.card == None:
            print("ERROR: Must register with a hospital first")
            return False
        
        response = self.send_msg(patient_msg.seek_treatment_msg(self.card_path), physician_address, physician_port)
        if isinstance(response , int):
            print("ERROR: Physician client error")
            return
 
       # Physician returns a boolean.
        if response.get(patient_msg.RESPONSE):
            print("Treatment done.")
            return True
        else:
            print("Unable to seek treatment.")
            return False
 

    def read(self, hospital_address, hospital_port):
        """
        Function for a patient to read all of their data.
        :param hospital_address: Hospital address
        :param hospital_port: Hospital port
        :return: nothing
        """       
        if self.card:
            socket = self.send_msg_get_socket(patient_msg.read(self.card.uid), hospital_address, hospital_port)
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
                        print(crypto.decrypt(response.get(patient_msg.BLOCK), self.card.priv_key))                
                        num_blocks = response.get(patient_msg.NUM_BLOCKS)
                        # Special casing the first response before reading the rest.
                        for i in range(1, num_blocks):
                            data = socket.recv(MESSAGE_SIZE)
                            if data:
                                responses = constants.deserialize(data)
                                for response in responses: 
       		                        print(crypto.decrypt(response.get(patient_msg.BLOCK), self.card.priv_key))
            
                    else:
                        print("No records were retrieved.")
                        break
            socket.close()

        else:
            print("ERROR: Must register with a hospital first")               

    def read_medical_record(self, physician, hospital):
        """
        Function for a patient to give a physician permission to read their data.
        :param physician: Physician
        :param hospital: Hospital
        :return: nothing
        """       
        if self.card:
            physician.read_patient_record(self.card, hospital)


    def remove(self, hospital):
        """
        Function for a patient to remove all of their data.
        :param hospital: Hospital
        :return: boolean
        """       
        if self.card:
            if hospital.remove(self.card):
                 return True
        return False

    def transfer(self, src_hospital, dst_hospital):
        """
        Function to transfer data to another hospital
        :param src_hospital: Current hospital
        :param dst_hospital: New hospital
        :return: boolean
        """       
        if self.card:
            if src_hospital.transfer(self.card, dst_hospital):
                 return True
        return False

    def transfer_medical_record(self, src_hospital, dst_hospital, physician):
        """
        Function for patient to give permission to physician to transfer medical records.
        :param src_hospital: Current hospital
        :param dst_hospital: New hospital
        :param physician: Physician
        :return: boolean
        """       
        if self.card:
            return physician.transfer_patient_record(self.card, src_hospital, dst_hospital)
        return False
