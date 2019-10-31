def write(uid_hash, new_block_payload):
    """
    1. Get the row using uid hash
    2. Create new block with payload and previous hash
    3. Insert block to end of linked list OR (maybe) stringified python list
    """
    pass

def get_last_block(uid_hash):
    """
    1. Return the last block in the row using the uid hash
    """
    pass


def delete(uid_hash, priv_key):
    """
    1. Get the row using uid hash
    2. Decrypt uid hash with priv_key
    3. If decrypted uid == uid, then nuke!
    """
    pass

def insert(uid_hash, patient_data_history):
    """
    1. Get the row using uid hash
    2. Insert patient_data_history
    """
    pass