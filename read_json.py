import json

with open('obj1.json', 'r') as f:
  data = json.load(f)

print(data)

import encrypt_json
import decrypt_json

obj_to_send = {
    "txn_id": "89798798",
    "src": "self.name",
    "dest": "org1",
    "src_data": None,
    "dest_data": b"sss".hex()
}

enc_msg = encrypt_json.encrypt_txn(str.encode(json.dumps(obj_to_send)),"org1")

dec_msg = decrypt_json.decrypt_txn(enc_msg,"org1")
print(json.loads(dec_msg.decode()))
