import sys
sys.path.insert(1,'/Users/saklain/Desktop/smart-city-off-chain-communication')
import encrypt_json
import decrypt_json
import json

from pysondb import db
json_db = db.getDb("offchain_db.json")
port_db = db.getDb("port_db.json")
# from pysondb import db
#
# a = db.getDb('offchain_db.json')
#
# print(a)
#
# a.add({'name':'pysondb','type':'DB'})
#
# b = a.getBy({"name":"pysondb"})
#
# print(b)


from pysondb import db
a=db.getDb("offchain_db.json")



txn = json_db.getByQuery({'txn_id': "b7e8ab9a-768b-11ed-b963-2614a5beb46e"})
txn = txn[0]
print("txn::: ",txn)


encrypted_src_data = bytes.fromhex(txn['src_data'])
print("encrypted_src_data:", encrypted_src_data)

decrypted_src_data = decrypt_json.decrypt_txn(encrypted_src_data, "org3")
decrypted_src_data = json.loads(decrypted_src_data)
print("###", decrypted_src_data)





# a.addMany([{"txn_id":"txn1","src":"sampleorg1","dest":"sampleorg2","src_data":"6767868", "dest_data":"875758578857"},
#             {"txn_id":"txn2","src":"sampleorg1","dest":"sampleorg3","src_data":"dadaf", "dest_data":"dadiutf98"}
#             ])
# print(a.getAll())
#
# k = a.getBy({'txn_id':'89798798'})
# print(k[0])
#
# encrypted_dest_data = bytes.fromhex(k[1]['src_data'])
# print("encrypted_dest_data:", encrypted_dest_data)
#
# decrypted_dest_data = decrypt_json.decrypt_txn(encrypted_dest_data, 'org2')
# print(json.loads(decrypted_dest_data))
#
#
# import uuid
# print(str(uuid.uuid1()))

# >> [{"name":"pysondb","type":"DB"},{"name":"pysondb-cli","type":"CLI"}]


# from pysondb import db
# a=db.getDb("port_db.json")
# a.addMany([{"org":"org1","port": 65001},
#             {"org":"org2","port": 65002},
#             {"org":"org3","port": 65000},
#             ])
# print(a.getAll())

#
# with open('obj1.json') as user_file:
#   file_contents = user_file.read()
#
# print(file_contents)

#
# import json
#
# with open('obj1.json', 'r') as f:
#   data = json.load(f)
#
# print(data, type(data))
