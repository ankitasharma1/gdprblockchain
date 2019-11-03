import hashlib as hasher

def hash(data):
    h = hasher.sha256()
    result = str(data)
    h.update(result.encode('utf-8'))
    return h.hexdigest()

