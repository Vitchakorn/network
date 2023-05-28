import socket
import threading
import time 

PORT = 9000
IP = ['172.28.5.1', '172.28.5.2', '172.28.5.3', '172.28.5.4']
host = socket.gethostname()
host_address = socket.gethostbyname(host)
index = 0 
graph = [[0, 10, 15, 20], [10, 0, 35, 25],
        [15, 35, 0, 30], [20, 25, 30, 0]]

def client(address):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((address, PORT))
            message = client_socket.recv(1024).decode()
            print(message)
            client_socket.close()
            break
        except Exception as e:
            continue


def handle_client(client_socket, client_address):
    node_host = IP.index(host_address)
    node_client = IP.index(client_address[0])
    cost = graph[node_host][node_client]
    message = str(node_host) + str(node_client) + " and cost is {}".format(cost) 
    client_socket.send(message.encode())


def server(address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, PORT))
    server_socket.listen()
    clients = 0
    while True:
        client_socket, client_address = server_socket.accept()
        time.sleep(1)
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        clients += 1
        if (clients == len(IP) - 1):
            break
    server_socket.close()


def main():
    global index
    if host_address == IP[index]:
        server(IP[index])
    else:
        client(IP[index])
    
    index += 1

    if (index != len(IP)):
        main()

main()
    
