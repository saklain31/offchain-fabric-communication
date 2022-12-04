import socket
from threading import Thread

class Org1:
    def __init__(self):
        self.name = "org2"
        self.host = 'localhost'  # Standard loopback interface address
        self.port = 65002        # Port to listen on (non-privileged ports are > 1023)

        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv.bind((self.host, self.port))
        self.serv.listen(3)

        print("Starting Organization on port:", self.port)

        server_thread=Thread(target=self.server)
        server_thread.start()

        client_thread=Thread(target=self.client)
        client_thread.start()

    def server(self):
        while True:
            conn, addr = self.serv.accept()
            # print(conn)
            # print(addr)
            data = conn.recv(4096)
            if not data:
                break
            print(data)
            conn.send(b"Acknowledgement from org2 ")

    def client(self):
        while True:
            dest_port = input("enter port: ")
            try:
                dest_port = int(dest_port)
                # print(dest_port)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.host, dest_port))
                client.send(b"msg from org2")
                from_server = client.recv(4096)
                print(from_server)
                client.close()
            except:
                print("Enter Integer Port")

Org1()
