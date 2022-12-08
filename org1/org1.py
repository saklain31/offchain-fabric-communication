import socket
from threading import Thread

import sys
sys.path.insert(1,'/Users/saklain/Desktop/smart-city-off-chain-communication')
import encrypt_json
import decrypt_json
import json
import uuid

from pysondb import db
json_db = db.getDb("offchain_db.json")
port_db = db.getDb("port_db.json")

class Org:
    def __init__(self):
        self.name = "org1"
        self.host = 'localhost'  # Standard loopback interface address
        self.port = 65001        # Port to listen on (non-privileged ports are > 1023)

        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv.bind((self.host, self.port))
        self.serv.listen(3)

        print("Starting Organization on port:", self.port)

        server_thread=Thread(target=self.server)
        server_thread.start()

        client_thread=Thread(target=self.client)
        client_thread.start()

    def read_json(file_path):
        import json

        with open('org1/data1.json', 'r') as f:
          data = json.load(f)

        print(data)


    def server(self):
        while True:
            conn, addr = self.serv.accept()

            data = conn.recv(4096)

            if not data:
                break
            print(data, type(data))
            json_obj = json.loads(data)

            if 'auth' in json_obj:
                print("Authority request")
                print("Txn_id:", json_obj['txn_id'])

                txn = json_db.getByQuery({'txn_id': json_obj['txn_id']})
                txn = txn[0]
                print("txn::: ",txn)

                if self.name == txn['src']:
                    encrypted_src_data = bytes.fromhex(txn['src_data'])
                    print("encrypted_src_data:", encrypted_src_data)

                    decrypted_src_data = decrypt_json.decrypt_txn(encrypted_src_data, self.name)
                    decrypted_src_data = json.loads(decrypted_src_data)
                    print("###", decrypted_src_data)

                    encrypted_auth_data = encrypt_json.encrypt_txn(str.encode(json.dumps(decrypted_src_data)),"auth")
                    print("encrypted_auth_data:", encrypted_auth_data.hex())
                    conn.sendall(bytes(json.dumps({"data": encrypted_auth_data.hex()}), encoding="utf-8"))

                elif self.name == txn['dest']:
                    encrypted_dest_data = bytes.fromhex(txn['dest_data'])
                    print("encrypted_dest_data:", encrypted_dest_data)

                    decrypted_dest_data = decrypt_json.decrypt_txn(encrypted_dest_data, self.name)
                    decrypted_dest_data = json.loads(decrypted_dest_data)
                    print("###", decrypted_dest_data)

                    encrypted_auth_data = encrypt_json.encrypt_txn(str.encode(json.dumps(decrypted_dest_data)),"auth")
                    print("encrypted_auth_data:", encrypted_auth_data.hex())
                    conn.sendall(bytes(json.dumps({"data": encrypted_auth_data.hex()}), encoding="utf-8"))

                else:
                    print("Invalid source!")

            else:
                print("json_obj", json_obj)

                encrypted_dest_data = bytes.fromhex(json_obj['dest_data'])
                print("encrypted_dest_data:", encrypted_dest_data)

                decrypted_dest_data = decrypt_json.decrypt_txn(encrypted_dest_data, self.name)
                decrypted_dest_data = json.loads(decrypted_dest_data.decode())
                print("decrypted_dest_data:", decrypted_dest_data)

                encrypted_src_data = encrypt_json.encrypt_txn(str.encode(json.dumps(decrypted_dest_data)),json_obj['src'])
                json_obj['src_data'] = encrypted_src_data.hex()

                print("whole obj:", json_obj)
                json_db.add(json_obj)

                conn.send(bytes("Acknowledgement from "+self.name,'utf-8'))

    def client(self):
        while True:
            choice = int(input("Enter your choice: "))
            if choice == 1: # Sending data to other org
                dest_org = input("Enter dest org: ")
                dest_port_obj = port_db.getBy({"org": dest_org})
                dest_port = dest_port_obj[0]['port']
                print("dest_port:", dest_port)

                obj_file = input("Enter data file name:")
                try:
                    dest_port = int(dest_port)
                    # print(dest_port)
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((self.host, dest_port))

                    try:
                        with open(obj_file) as file:
                          file_obj = json.load(file)
                        print(file_obj, type(file_obj))
                        try:
                            encrypted_obj = encrypt_json.encrypt_txn(str.encode(json.dumps(file_obj)), dest_org)
                            print("encrypted: ", encrypted_obj)
                        except Exception as e:
                            print("Encryption failed!", e)
                    except:
                        print("Data file not found!")
                        continue

                    obj_to_send = {
                        "txn_id": str(uuid.uuid1()),
                        "src": self.name,
                        "dest": dest_org,
                        "src_data": None,
                        "dest_data": encrypted_obj.hex()
                    }

                    print(obj_to_send, type(obj_to_send))
                    print("$$$$")
                    # print(str.encode(json.dumps(obj_to_send)), type(str.encode(json.dumps(obj_to_send))))

                    # client.send(b"ss")
                    client.sendall(bytes(json.dumps(obj_to_send), encoding="utf-8"))

                    print("****")
                    from_server = client.recv(4096)
                    print(from_server)
                    client.close()

                except:
                    print("Enter Integer Port")

            elif choice == 2:
                txn_id = input("Insert txn_id:")
                txn = json_db.getByQuery({'txn_id': txn_id})
                txn = txn[0]
                print("txn::: ",txn)

                if self.name == txn['src']:
                    encrypted_src_data = bytes.fromhex(txn['src_data'])
                    print("encrypted_src_data:", encrypted_src_data)

                    decrypted_src_data = decrypt_json.decrypt_txn(encrypted_src_data, self.name)
                    decrypted_src_data = json.loads(decrypted_src_data)
                    print("###", decrypted_src_data)

                elif self.name == txn['dest']:
                    encrypted_dest_data = bytes.fromhex(txn['dest_data'])
                    print("encrypted_dest_data:", encrypted_dest_data)

                    decrypted_dest_data = decrypt_json.decrypt_txn(encrypted_dest_data, self.name)
                    decrypted_dest_data = json.loads(decrypted_dest_data)
                    print("###", decrypted_dest_data)
                else:
                    print("Not authorized!!")

            else:
                print("Invalid choice")

Org()
