class Patient:
    def __init__(self, name, gov_id):
        self.name = name
        self.gov_id = gov_id
        self.uid = gov_id + name
        # TODO: Stretch Goal - keep track of their own records
        self.record_path = None
        self.card_path = None

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


class Card:
    def __init__(self, path):
        self.path = path
        self. populate()
        self.priv_key = None
        self.uid = None
        self.hospital_id = None

    def populate(self):
        # TODO: Open the path and populate card params
        pass

    def update(self, hospital_id):
        self.hospital_id = hospital_id

class MedicalRecord:
    def __init__(self):
        pass

    # REPL for commands