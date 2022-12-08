from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def read_public_key(org):
  return RSA.import_key(open(org+'_public_pem.pem', 'r').read())

def encrypt_txn(obj, org):
    pu_key = read_public_key(org)

    #Instantiating PKCS1_OAEP object with the public key for encryption
    cipher = PKCS1_OAEP.new(key=pu_key)

    #Encrypting the message with the PKCS1_OAEP object
    cipher_text = cipher.encrypt(obj)
    return cipher_text
