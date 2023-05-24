import socket
import threading

PORT = 1234
IP = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
host_name = socket.gethostname()
host_address = socket.gethostbyname(host_name)
print(host_address)

def server(address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, PORT))
    server_socket.listen()
    clients = 0 
    while True:
        client_socket, client_address = server_socket.accept()
        print("cli_address :" + client_address)
        print("cli_socket :" + client_socket)
        message = "received node" + str(IP.index(host_address)) + " from " + host_address
        client_socket.send(message.encode())
        client_socket.close()
        clients += 1
        if clients >=3:
            return False
    server_socket.close()

        



def client(address) :
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, PORT))
    message = client_socket.recv(1024).encode('utf-8')
    print(message)
    client_socket.close()


server(IP[0])
client(IP[1])

print(host_address)