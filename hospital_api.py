# Register
def register(patient_uid):
    """
    1. Use hasher to get index for uid
    2. Looks this up in public blockchain
    3. If id already exists, reject
    4. If not, generate pub/priv key pair
    5. Encrypt patient UID with pub key and add transaction to public blockchain
    6. write(uid, priv_key) creating the genesis patient block
    7. Generate object file (card) and return to patient
    """
    pass

# Write
def write(uid, priv_key, med_record):
    """
    1. Use hasher to get index for uid
    2. Get this block from public blockchain
    3. Get last block from the hospital db
    4. Decrypt last block with priv_key
    5. Create new block consisting of old_block_data + med_record
    6. Encrypt new block with pub_key
    7. Send encrypted new block to db to be appended 
    """
    pass

# Read
def read(uid, priv_key):
    """
    1. Use hasher to get index for uid
    2. Get this block from public blockchain
    3. Get last block from the hospital db
    4. Decrypt last block with private key
    5. Return block to whoever requested    
    """
    pass

# Remove
def remove(uid, priv_key):
    """
    1. Use hasher to get index for uid
    2. Get this block from public blockchian
    3. Call remove for hospital db(uid)
    """    
    pass

# Transfer
def transfer(src_hosptial_id, dest_hosptial_id, uid, card):
    """
    1. Use hasher to get index for uid
    2. Get this block from public blockchain
    3. Get the last block from the hospital source db
    4. Call transfer_write() with dest hospital id, uid, and encrypted block
    5. Tell patient to remove data from src_hosptial, tell dest_hosptial_id to generate
    new card for patient
    6. update_card(card) - Update with dest_hospital_id
    """    
    pass

def transfer_write(dest_hospital_id, uid, block):
    """
    1. Append block to dest_hosptial_id using uid as row selector
    """    
    pass

def update_card(card):
    """
    1. Change hospital id to its own and update card 
    """
    pass