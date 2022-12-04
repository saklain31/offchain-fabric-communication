import socket
from threading import Thread

class Org1:
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
            # print(conn)
            # print(addr)
            data = conn.recv(4096)
            # Write: IF data(=encrypted by pubkey of this peer) coming from another peer as transaction:
                # decrypt using own privkey
                # encrypt using own privkey
                # encrypt using sender's pubkey
                # store

            if not data:
                break
            print(data)
            conn.send(b"Acknowledgement from org1 ")

    # def read_data(tx_id):
        # if tx_id.dest == self: then: send to source for decryption
        # if tx_id.source == self: then: double decryption


    def client(self):
        while True:
            dest_port = input("enter port: ")
            try:
                dest_port = int(dest_port)
                # print(dest_port)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.host, dest_port))
                client.send(b"msg from org1")
                from_server = client.recv(4096)
                print(from_server)
                client.close()
            except:
                print("Enter Integer Port")

Org1()
