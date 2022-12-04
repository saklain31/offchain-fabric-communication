from Crypto.PublicKey import RSA
from os.path import exists

def generate_keys(org):
    if not exists(org+'_public_pem.pem'):
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()

        #Converting the RsaKey objects to string
        private_pem = private_key.export_key().decode()
        public_pem = public_key.export_key().decode()

        with open(org+'/'+ org +'_private_pem.pem', 'w') as pr:
          pr.write(private_pem)
        with open(org+'_public_pem.pem', 'w') as pu:
          pu.write(public_pem)
    else:
        print("Keys already exist!!")
        print("No key is created")

folder = input("Enter Org Name:")
print(folder)
generate_keys(folder)
