import socket
import sys
from patient import Patient
from parser import Parser
from threading import Thread
from threading import Condition
from constants import ADDRESS
from constants import PORT
from constants import MESSAGE_SIZE
import constants

"""
Supported Commands
"""
EXIT = 'exit'
REGISTER = 'reg'
READ = 'rd'
PHYS_READ = 'phys_rd'
REMOVE = 'rm_records'
TREATMENT = 'treatment'
TRANSFER = 'transfer'
PHYS_TRANSFER = 'phys_transfer'
PHYSICIANS = 'phys'
HOSPITALS = 'hosp'
CARD = 'card'
REMOVE_CARD = 'rm_card'

"""
Supported Commands Params
"""
NUM_REGISTER_PARAMS = 2 # 'reg [hospital_name]'
NUM_TREATMENT_PARAMS = 2 # 'treatment [physician_name]' 
NUM_READ_PARAMS = 2 # 'rd [hospital_name]'
NUM_PHYS_READ_PARAMS = 2 # 'phys_rd [physician_name]'
NUM_RM_PARAMS = 2 # 'rm [hospital_name]'
NUM_TRANSFER_PARAMS = 3 # 'transfer [src_hospital_name] [dst_hospital_name]
NUM_PHYS_TRANSFER_PARAMS = 3 # 'phys_transfer' [src_hospital_name] [physician_name]

p = None
parser = Parser()

def main():
    """
    Wrapper around the patient class.
    """
    arguments = sys.argv
    if len(arguments) < 2:
        print("ERROR: missing argument - %s" %(parser.get_patient_names_string()))
        return

    patient_name = arguments[1]

    if not parser.valid_patient(patient_name):
        print("ERROR: invalid argument - %s" %(parser.get_patient_names_string()))
        return

    # Construct patient using info. from parser.
    global p
    p = Patient(patient_name, parser.get_patient_id(patient_name))
    p.set_card_path(parser.get_patient_card(patient_name))
    contact_info = parser.get_patient_contact_info(patient_name)
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
    print("Starting repl for %s." %(patient_name))
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
            elif command == PHYSICIANS:
                print(parser.get_phys_names_string())
            elif command == HOSPITALS:
                print(parser.get_hosp_names_string())
            elif command == REGISTER:
                if len(commands) != NUM_REGISTER_PARAMS:
                    print("Usage: %s [hospital_name]" %(REGISTER))
                    continue
                hospital_name = commands[1]
                register(hospital_name)
            elif command == CARD:
                print(str(p.card) + "\n")
            elif command == TREATMENT:
                if len(commands) != NUM_TREATMENT_PARAMS:
                    print("Usage: %s [physician_name]" %(TREATMENT))
                    continue
                physician_name = commands[1]
                treatment(physician_name)  
            elif command == READ: 
                if len(commands) != NUM_READ_PARAMS:
                    print("Usage: %s [hospital_name]" %(READ))
                    continue
                hospital_name = commands[1]
                read(hospital_name)       
            elif command == PHYS_READ: 
                if len(commands) != NUM_PHYS_READ_PARAMS:
                    print("Usage: %s [physician_name]" %(PHYS_READ))
                    continue
                phys_name = commands[1]
                phys_read(phys_name)             
            elif command == REMOVE_CARD:
                print("Removing card...\n")
                p.card = None
            elif command == REMOVE:
                if len(commands) != NUM_RM_PARAMS:
                    print("Usage: %s [hospital_name]" %(REMOVE))
                    continue
                hospital_name = commands[1]
                print("Requesting to remove all records...\n")
                remove(hospital_name)
            elif command == TRANSFER:
                if len(commands) != NUM_TRANSFER_PARAMS:
                    print("Usage: %s [src_hospital_name] [dest_hospital_name]" %(TRANSFER))
                    continue
                src_hospital_name = commands[1]
                dest_hospital_name = commands[2]
                transfer(src_hospital_name, dest_hospital_name) 
            elif command == PHYS_TRANSFER:
                if len(commands) != NUM_PHYS_TRANSFER_PARAMS:
                    print("Usage: %s [src_hospital_name] [phys_name]" %(PHYS_TRANSFER))
                    continue
                src_hospital_name = commands[1]
                phys_name = commands[2]
                phys_transfer(src_hospital_name, phys_name)           
            else:
                print("Supported Commands: [" + EXIT + ", " + PHYSICIANS + ", " + REMOVE + ", " + READ + ", " + PHYS_READ + ", " + HOSPITALS + ", " + CARD + ", " + REMOVE_CARD + ", " + REGISTER + ", " + TRANSFER + ", " + PHYS_TRANSFER + "]")
        except Exception, e:
            print(e)

def phys_transfer(src_hospital_name, phys_name):
    if not parser.valid_hosp(src_hospital_name):
        print("ERROR: invalid src_hospital_name - %s" %(parser.get_hosp_names_string()))
        return

    if not parser.valid_phys(phys_name):
        print("ERROR: invalid physician name - %s" %(parser.get_phys_names_string()))
        return

    phys_contact_info = parser.get_phys_contact_info(phys_name)
    p.phys_transfer(src_hospital_name, phys_contact_info[ADDRESS], phys_contact_info[PORT])    

def transfer(src_hospital_name, dest_hospital_name):
    if not parser.valid_hosp(src_hospital_name):
        print("ERROR: invalid src_hospital_name - %s" %(parser.get_hosp_names_string()))
        return
    if not parser.valid_hosp(dest_hospital_name):
        print("ERROR: invalid dest_hospital_name - %s" %(parser.get_hosp_names_string()))
        return
    if src_hospital_name == dest_hospital_name:
        print("ERROR: unsupported transfer request")
        return

    src_hosp_contact_info = parser.get_hosp_contact_info(src_hospital_name)
    p.transfer(src_hosp_contact_info[ADDRESS], src_hosp_contact_info[PORT], dest_hospital_name)
    return

def remove(hosp_name):
    if not parser.valid_hosp(hosp_name):
        print("ERROR: invalid hospital - %s" %(parser.get_hosp_names_string()))
        return

    hosp_contact_info = parser.get_hosp_contact_info(hosp_name)
    p.remove(hosp_contact_info[ADDRESS], hosp_contact_info[PORT])
    return


def phys_read(phys_name):
    if not parser.valid_phys(phys_name):
        print("ERROR: invalid physician name - %s" %(parser.get_phys_names_string()))
        return

    phys_contact_info = parser.get_phys_contact_info(phys_name)
    p.phys_read(phys_contact_info[ADDRESS], phys_contact_info[PORT])
    return

def read(hosp_name):
    if not parser.valid_hosp(hosp_name):
        print("ERROR: invalid hospital - %s" %(parser.get_hosp_names_string()))
        return

    hosp_contact_info = parser.get_hosp_contact_info(hosp_name)
    p.read(hosp_contact_info[ADDRESS], hosp_contact_info[PORT])
    return

def treatment(phys_name):
    if not parser.valid_phys(phys_name):
        print("ERROR: invalid physician name - %s" %(parser.get_phys_names_string()))
        return

    phys_contact_info = parser.get_phys_contact_info(phys_name)
    p.seek_treatment(phys_contact_info[ADDRESS], phys_contact_info[PORT])
    return

def register(hosp_name):
    if not parser.valid_hosp(hosp_name):
        print("ERROR: invalid hospital - %s" %(parser.get_hosp_names_string()))
        return

    hosp_contact_info = parser.get_hosp_contact_info(hosp_name)
    p.register(hosp_contact_info[ADDRESS], hosp_contact_info[PORT])
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
                    print(message)
            else:
                return clean_up(c)
        except Exception, e:
            print(e)
            return clean_up(c)

def clean_up(c):
    print("Closing connection")
    c.close()

main()
    
