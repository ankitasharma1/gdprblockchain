from time import time
import datetime
import hashlib as hasher

""" Class for transactions made on the blockchain. Each transaction has a
    sender, recipient, and value.
    """
class Transaction:
    
    """ Transaction initializer """
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
    
    """ Converts the transaction to a dictionary """
    def toDict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'value': self.value
    }

    def __str__(self):
        toString = self.sender + " -> " + self.recipient + " (" + self.value + ") "
        return toString;

""" Class for Blocks. A block is an object that contains transaction information
    on the blockchain.
    """
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time()
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0 
        self.time_string = self.timestamp_to_string();

    # Function to compute a blocks hash.
    def compute_hash(self):
        # Update crypt hash with index, time,
        # prev hash, data, and nonce
        h = hasher.sha256()
        
        index = str(self.index)
        timestamp = self.time_string
        prev_hash = str(self.previous_hash)
        data = str(self.data)
        nonce = str(self.nonce)
        
        result = index + timestamp + prev_hash + data + nonce              
        h.update(result)
        return h.hexdigest()
                
    """ Function to convert a timestamp to a string"""
    def timestamp_to_string(self):
        return datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M')
    
    def __str__(self):
        toString =  str(self.index) + "\t" + str(self.timestamp) +"\t\t" + str(self.previous_hash) + "\n"
        for tx in self.data:
            toString +=  "\t" + str(tx) + "\n"
        return toString;

""" Blockchain class. The blockchain is the network of blocks containing all the
    transaction data of the system.
    """
class Blockchain:
    def __init__(self):
        self.difficulty = 4
        self.unconfirmed_transactions = []
        self.chain = []
        
        if (self.create_genesis_block() < 0):
            print("ERROR creating genesis block")
            exit()
        
    # Function to create the genesis block.                
    def create_genesis_block(self):
        genesis_block = Block(0, [], 0)
        # Add block to blockchain
        return self.perform_and_add(genesis_block)
    
    # Function to add a new transaction.
    def new_transaction(self, sender, recipient, value):
        transaction = Transaction(sender, recipient, value)
        # Add it to list of unconfirmed transactions as a dictionary
        self.unconfirmed_transactions.append(transaction.toDict())
        # Return transaction object
        return transaction;
    
    # Function to mine.
    def mine(self):
        if(len(self.unconfirmed_transactions) > 0) :
            # Grab a transaction
            transaction = self.unconfirmed_transactions.pop(0)
            index = self.get_next_index()
            # Create a new block
            new_block = Block(index, transaction.get('value'), self.get_hash(index - 1))
            # Add block to blockchain
            if (self.perform_and_add(new_block) < 0):
                print("ERROR adding block in mine()")
            # Return newly created block
            return new_block 
        else:
            print("ERROR no blocks to mine")
    
    # Helper function to call proof_of_work() and add_to_block()
    # since these steps go together.
    def perform_and_add(self, block):
        self.proof_of_work(block)
        # Add block to blockchain
        if (self.add_block(block)):
            return 0
        return -1
            
    # Helper function to get the index of the next block.
    def get_next_index(self):
        return len(self.chain)
        
    # Helper function to return hash associated with a block.    
    def get_hash(self, index):
        block = self.chain[index]
        return block.compute_hash()
    
    # Helper function to get hash of last block in chain.
    def get_last_hash(self):
        last = len(self.chain) - 1
        return self.chain[last].compute_hash()
    
    # Function to find nonce to create desired
    # hash.
    def proof_of_work(self, block):
        while True:
            if (self.validate_hash(block)):
                return block.compute_hash()
            else:
                block.nonce = block.nonce + 1
    
    # Function to add a block to the blockchain.
    def add_block(self, block):
        # If genesis block, add it
        if block.index == 0:
            self.chain.append(block)
            return True
        if (block.previous_hash == self.get_last_hash()):
            self.chain.append(block)
            return True        
        return False
    
    # Function to check integrity of blockchain.
    def check_integrity(self):
        index = 0
        prev_block = None
        
        for block in self.chain:
            # Each block is indexed one after the other
            if block.index != index:
                print("ERROR incorrect index - block is: " + str(block.index) + " should be: " + str(index))
                return False
            # Each block's previous hash is the hash of the
            # previous block
            if prev_block == None:
                prev_block = block
            else:
                if block.previous_hash != prev_block.compute_hash():
                    print("ERROR incorrect hash - block prev hash: " + block.previous_hash + " should be: " + prev_block.compute_hash())                
                    return False
                prev_block = block
            # Block's hash is valid given the set difficulty
            if self.validate_hash(block) == False:
                print("ERROR invalid hash")             
                return False
                
            index = index + 1
            
        return True
    
    # Helper function to validate the hash given the difficulty.
    def validate_hash(self, block):
        computed_hash = block.compute_hash()
        diff = "0" * self.difficulty
        if (computed_hash[:self.difficulty] != diff):
            return False
        return True

    """ Function that returns the last block on the chain"""
    @property
    def last_block(self):
        return self.chain[-1]
