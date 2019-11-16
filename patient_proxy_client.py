import sys
from patient import Patient
from parser import Parser

"""
Supported Commands
"""
EXIT = 'exit'
REGISTER = 'reg'
REMOVE = 'rm'
TREATMENT = 'treatment'
TRANSFER = 'transfer'
DOCTORS = 'docs'
HOSPITALS = 'hosp'

p = None
parser = Parser()
address = None
port = None

def main():
    """
    Wrapper around the patient class.
    """
    arguments = sys.argv
    if len(arguments) < 2:
        print("ERROR: missing argument %s" %(', '.join(parser.get_patient_names()))
        return

    patient_name = arguments[1]
    print("Starting repl for %s." %(patient_name))

    if not parser.valid_patient(patient_name):
        #print("ERROR: incorrect argument %s" %(parser.get_patient_names())
        return

    # Create socket object.
    s = socket.socket()
    s.bind(('', port))
    print("Socket binded to %s" %(port))

    # Put the socket into listening mode.        
    s.listen(5)
    print("Socket is listening")

    # Spawn repl thread.
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
            elif command == PRINT:
                bc.print_blockchain()
            else:
                print("Supported Commands: " + EXIT + " " + PRINT)
        except Exception, e:
            pass

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
            data = c.recv(bc_msg.MESSAGE_SIZE)
            if data:
                messages = bc_msg.deserialize(data)
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
    
