import crypto
from Crypto.PublicKey import RSA

def main():
    priv_key, pub_key = crypto.generate_keys()

    pem = priv_key.exportKey(format='PEM', passphrase=None, pkcs=1)
    with open("trash.pem", 'wb') as f:
        f.write(pem)
        f.close()

    encrypted = crypto.encrypt("hiiiiii", pub_key)
    
    with open("trash.pem", "r") as filestream:
        content = filestream.read()
        content.replace("-----BEGIN RSA PRIVATE KEY-----", "")
        content.replace("-----END RSA PRIVATE KEY-----", "")
        priv_key = RSA.importKey(content, passphrase=None)

    decrypted = crypto.decrypt(encrypted, priv_key)
    print(decrypted)

main()
