from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA



def read_private_key():
    return RSA.import_key(open('org1/org1_private_pem.pem', 'r').read())

def decrypt_txn(obj):
    pr_key = read_private_key()

    decrypt = PKCS1_OAEP.new(key=pr_key)

    #Decrypting the message with the PKCS1_OAEP object
    decrypted_message = decrypt.decrypt(obj)
    return decrypted_message
