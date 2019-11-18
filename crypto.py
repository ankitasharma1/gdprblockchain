# gist.github.com/syedrakib/241b68f5aeaefd7ef8e2

from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def generate_keys():
    modulus_length = 256 * 4
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey

def encrypt(message, publickey):
    encrypted_msg = publickey.encrypt(message, 32)[0]
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    return encoded_encrypted_msg

def decrypt(encoded_encrypted_msg, privatekey):
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
    return decoded_decrypted_msg

def retrieve_private_key(path):
    with open(path, "r") as f:
        content = f.read()
        content.replace("-----BEGIN RSA PRIVATE KEY-----", "")
        content.replace("-----END RSA PRIVATE KEY-----", "")
        priv_key = RSA.importKey(content, passphrase=None)
        f.close()
        return priv_key

def store_private_key(path, priv_key):
    pem = priv_key.exportKey(format='PEM', passphrase=None, pkcs=1)
    with open(path, 'wb') as f:
        f.write(pem)
        f.close()
