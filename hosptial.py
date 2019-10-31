class Hosptial:
    def __init__(self, blockchain, hasher, db):
        # TODO: Use uuid()
        self.id = None
        # TODO: Import our hash lib that will take care of this
        self.hasher_key = None # ex: hasher.add_key()
        self.blockchain = blockchain
        self.db = db

# updates, connections from patient, requests, i sent this etc. this one failed.