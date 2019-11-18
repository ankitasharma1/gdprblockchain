import socket
import sys
from constants import ADDRESS
from constants import PORT
from parser import Parser
from threading import Thread
from threading import Condition
from physician import Physician
from constants import MESSAGE_SIZE
from constants import TYPE
import constants
import patient_msg
import card_helper

"""
Supported Commands
"""
EXIT = 'exit'
REGISTER = 'reg'
HOSPITALS = 'hospitals'

"""
Supported Commands Params
"""
NUM_REGISTER_PARAMS = 2 # 'reg [hospital name]'

phys = None
parser = Parser()

def main():
    """
    Wrapper around the physician class.
    """
    arguments = sys.argv
    if len(arguments) < 2:
        print("ERROR: missing argument - %s" %(parser.get_phys_names_string()))
        return

    physician_name = arguments[1]

    if not parser.valid_phys(physician_name):
        print("ERROR: invalid argument - %s" %(parser.get_phys_names_string()))
        return

    # Construct physician using info. from parser.
    global phys
    phys = Physician(physician_name, parser.get_phys_id(physician_name))
    contact_info = parser.get_phys_contact_info(physician_name)
    address = contact_info[ADDRESS]
    port = contact_info[PORT]

    # Condition variable for clean termination.
    cv = Condition()

    # Create socket object.
    s = socket.socket()
    s.bind(('', port))
    print("Socket binded to %s" %(port))

    # Put the socket into listening mode.        
    s.listen(5)
    print("Socket is listening")

    # Spawn repl thread.
    print("Starting repl for %s." %(physician_name))
    t = Thread(target=repl, args=(s, cv))
    t.daemon = True
    t.start()

    # Spawn connection thread.
    t = Thread(target=handle_connection, args=(s,))
    t.daemon = True
    t.start()

    # Wait for termination.
    termination = False    
    cv.acquire()
    while not termination:
        cv.wait()
        termination = True
        cv.release()

def repl(s, cv):
    print("Kicking off REPL\n\n")
    while True:
        commands = sys.stdin.readline().split()
        try:
            command = commands[0]
            if command == EXIT:
                # Close the socket.
                s.close()
                cv.acquire()
                # Notify main thread that user would like to exit.
                cv.notify()
                cv.release()
                return
            elif command == REGISTER:
                if len(commands) != NUM_REGISTER_PARAMS:
                    print( "Usage: reg [hospital name]")
                    continue
                hospital_name = commands[1]
                register(hospital_name)
            elif command == HOSPITALS:
                print(phys.get_hospitals())            
            else:
                print("Supported Commands: [" + EXIT + ", " + HOSPITALS + ", " + REGISTER + "]")
        except Exception, e:
            print(e)

def register(hosp_name):
    if not parser.valid_hosp(hosp_name):
        print("ERROR: invalid hospital - %s" %(parser.get_hosp_names_string()))
        return

    hosp_contact_info = parser.get_hosp_contact_info(hosp_name)
    phys.register(hosp_name, hosp_contact_info[ADDRESS], hosp_contact_info[PORT])
    return

def handle_connection(s):
    while True:
        try:
            c, addr = s.accept()
            print("Got connection from " + addr[0] + ": " + str(addr[1]))
            # Start a thread for each socket.
            t = Thread(target=listen_on_socket, args=(c,))
            t.daemon = True
            t.start()
        except Exception, e:
            #print(e)
            return

def listen_on_socket(c):
    while True:
        try:
            data = c.recv(MESSAGE_SIZE)
            if data:
                messages = constants.deserialize(data)
                for message in messages:
                    response = handle_message(message)
                    c.send(response)
            else:
                return clean_up(c)
        except Exception, e:
            print(e)
            return clean_up(c)

def handle_message(message):
    type = message.get(TYPE)
    if type == patient_msg.SEEK_TREATMENT:
        card_path = message.get(patient_msg.CARD_PATH)
        card = card_helper.get_card_object(card_path)
        print("-------> Request for treatment from %s" %(card.patient_name))
        # API Call #
        hosp_contact_info = parser.get_hosp_contact_info(card.hospital_name)
        if phys.seek_treatment(card_path, hosp_contact_info[ADDRESS], hosp_contact_info[PORT]):
            return patient_msg.seek_treatment_msg_response(True)
        return patient_msg.seek_treatment_msg_response(False)   
    elif type == patient_msg.PHYS_READ:
        card_path = message.get(patient_msg.CARD_PATH)
        card = card_helper.get_card_object(card_path)
        print("-------> Request to read medical records for %s" %(card.patient_name))
        # API Call #
        hosp_contact_info = parser.get_hosp_contact_info(card.hospital_name)
        if phys.read_patient_record(card_path, hosp_contact_info[ADDRESS], hosp_contact_info[PORT]):
            return patient_msg.phys_read_response_msg(True)
        return patient_msg.phys_read_response_msg(False)   
    else:
        print("ERROR: unknown type %s" %(type))

def clean_up(c):
    print("Closing connection")
    c.close()


main()
