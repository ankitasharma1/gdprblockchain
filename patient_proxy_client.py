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
REMOVE = 'rm'
TREATMENT = 'treatment'
TRANSFER = 'transfer'
PHYSICIANS = 'phys'
HOSPITALS = 'hosp'
CARD = 'card'

"""
Supported Commands Params
"""
NUM_REGISTER_PARAMS = 2 # 'reg [hospital name]'

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
    print("Kicking off REPL")
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
                    print( "Usage: reg [hospital name]")
                    continue
                hospital_name = commands[1]
                register(hospital_name)
            elif command == CARD:
                print(str(p.card))
            else:
                print("Supported Commands: [" + EXIT + ", " + PHYSICIANS + ", " + HOSPITALS + ", " + CARD + ", " + REGISTER +"]")
        except Exception, e:
            print(e)

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
    
