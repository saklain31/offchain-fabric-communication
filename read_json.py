import json

with open('data1.json', 'r') as f:
  data = json.load(f)

print(data)

import encrypt_json
import decrypt_json

enc_msg = encrypt_json.encrypt_txn(str.encode(json.dumps(data)))

dec_msg = decrypt_json.decrypt_txn(enc_msg)
print(json.loads(dec_msg.decode()))
