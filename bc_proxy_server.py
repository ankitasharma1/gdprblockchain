from blockchain import Blockchain
import socket
from threading import Thread
from threading import Condition
import sys
import bc_msg

"""
Supported Commands
"""
EXIT = 'exit'

def main():
    """
    Accepts requests to add blocks to the blockchain.
    """
    bc = Blockchain()

    # TODO: Port should be passed in as parameters.
    address = 'localhost'
    port = 1025
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
                print("Supported Commands: " + EXIT)
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
    size = bc_msg.MESSAGE_SIZE

    while True:
        try:
            data = c.recv(size)
            if data:
                messages = bc_msg.deserialize(data)
                for message in messages:
                    print(message)
            else:
                return clean_up(c)
        except Exception, e:
            return clean_up(c)

def clean_up(c):
    print("Closing connection")
    c.close()
main()
