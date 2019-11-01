import socket
from threading import Thread

class Hospital:
    def __init__(self, blockchain, hasher, db):
        # TODO: Use uuid()
        self.id = None
        # TODO: Import our hash lib that will take care of this
        self.hasher_key = None # ex: hasher.add_key()
        self.blockchain = blockchain
        self.db = db
        self.address = None
        self.port = None

    def set_address(self, address):
        self.address = address

    def set_port(self, port):
        self.port = port

    def handle_connection(self):
        # Create socket object.
        s = socket.socket()
        s.bind(('', self.port))
        s.listen(5)
        while True:
            c, addr = s.accept()
            print("Got connection from " + addr[0] + ": " + str(addr[1]))
            # Spawn thread to handle communication for each socket.
            t = Thread(target=self.listen_on_socket, args=(c,))
            t.start()

    def listen_on_socket(self, socket):
        while True:
            x = 5

    def clean_up(self):
        self.db.close()







# updates, connections from patient, requests, i sent this etc. this one failed.