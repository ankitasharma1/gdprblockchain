from blockchain import Blockchain
import socket
from threading import Thread
from threading import Condition
import sys
import bc_msg
from Crypto.PublicKey import RSA
from constants import MESSAGE_SIZE

"""
Supported Commands
"""
EXIT = 'exit'
PRINT = 'print'

bc = Blockchain()

def main():
    """
    Accepts requests to add blocks to the blockchain.
    """
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
            elif command == PRINT:
                bc.print_blockchain()
            else:
                print("Supported Commands: [" + EXIT + ", " + PRINT + "]")
        except Exception as e:
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
        except Exception as e:
            #print(e)
            return

def listen_on_socket(c):
    while True:
        try:
            data = c.recv(MESSAGE_SIZE)
            if data:
                messages = bc_msg.deserialize(data)
                for message in messages:
                    # If we are expecting to receive a public key.
                    if bc_msg.bc_expecting_pub_key(bc_msg.deserialize(data)):
                        # Wait for it.
                        pub_key = RSA.importKey(c.recv(1024), passphrase=None)
                        # Update the payload.
                        message.update({bc_msg.PUB_KEY:pub_key})
                    response = handle_message(message)
                    if response:
                        # Send public key if hospital is expecting it.
                        if bc_msg.hosp_expecting_pub_key(bc_msg.deserialize(data)):
                            c.send(response.exportKey(format='PEM', passphrase=None, pkcs=1))
                        else:
                            c.send(response)
            else:
                return clean_up(c)
        except Exception as e:
            print(e)
            return clean_up(c)

def handle_message(message):
    type = message.get(bc_msg.TYPE)
    if type == bc_msg.CONTAINS_HASH_UID:
        hash_uid = message.get(bc_msg.HASH_UID)
        print("-------> Servicing request to check if %s exists in the blockchain" %(hash_uid))
        response = bc.contains_hash_uid(hash_uid)
        return bc_msg.contains_hash_uid_msg_response(response)
    elif type == bc_msg.GET_PUB_KEY:
        hash_uid = message.get(bc_msg.HASH_UID)
        print("-------> Servicing request to obtain block for %s" %(hash_uid))
        pub_key = bc.get_pub_key(hash_uid)
        print("Returning %s " %(pub_key))
        return pub_key
    elif type == bc_msg.NEW_TXN:
        hash_uid = message.get(bc_msg.HASH_UID)
        pub_key = message.get(bc_msg.PUB_KEY)
        print("-------> Servicing request to insert new transaction with hash_uid:%s pub_key:%s" %(hash_uid, pub_key))
        bc.new_transaction(hash_uid, pub_key)
        return None
    elif type == bc_msg.MINE:
        print("-------> Servicing request to mine the blockchain")
        bc.mine()
        return None
    else:
        print("Unable to service request, invalid message: %d" %(type))

def clean_up(c):
    print("Closing connection")
    c.close()

main()
