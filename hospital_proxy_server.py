import socket
import sys
from hospital import Hospital
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

h = None
parser = Parser()

def main():
    """
    Wrapper around the patient class.
    """
    arguments = sys.argv
    if len(arguments) < 2:
        print("ERROR: missing argument - %s" %(parser.get_hosp_names_string()))
        return

    hospital_name = arguments[1]

    if not parser.valid_hosp(hospital_name):
        print("ERROR: invalid argument - %s" %(parser.get_hosp_names_string()))
        return

    # Construct patient using info. from parser.
    h = Hospital(hospital_name, parser.get_bc_contact_info()[ADDRESS], parser.get_bc_contact_info()[PORT])
    contact_info = parser.get_hosp_contact_info(hospital_name)
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
    print("Starting repl for %s." %(hospital_name))
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
            else:
                print("Supported Commands: [" + EXIT +"]")
        except Exception, e:
            print(e)

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
    
