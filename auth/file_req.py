import socket
import json
import sys
sys.path.insert(1,'/Users/saklain/Desktop/smart-city-off-chain-communication')
import encrypt_json
import decrypt_json
import json
import uuid

from pysondb import db
json_db = db.getDb("offchain_db.json")
port_db = db.getDb("port_db.json")

org_name = input("Enter org name:")
port_obj = port_db.getBy({"org": org_name})
org_port = port_obj[0]['port']

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', org_port))

txn_id = input("Insert txn_id:")

obj_to_send = {
    "txn_id": txn_id,
    "auth": True,
}

client.sendall(bytes(json.dumps(obj_to_send), encoding="utf-8"))
recv = client.recv(4096)
encrypted_data = bytes.fromhex(json.loads(recv)['data'])
print(encrypted_data)

decrypted_data = decrypt_json.decrypt_txn(encrypted_data, 'auth')
decrypted_data = json.loads(decrypted_data.decode())
print(decrypted_data)
