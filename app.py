import socket
import threading

PORT = 9000
IP = ['172.16.238.10', '172.16.238.11', '172.16.238.12', '172.16.238.13']
host_name = socket.gethostname()
host_address = socket.gethostbyname(host_name)
addr_index = 0 
graph = [[0, 10, 15, 20], [10, 0, 35, 25],
        [15, 35, 0, 30], [20, 25, 30, 0]]
total_cost = 0


def handle_client(client_socket, client_address):
    total_cost = 0
    node_host = IP.index(host_address)
    node_client = IP.index(client_address[0])
    cost = graph[node_host][node_client]
    total_cost += cost
    message = str(node_host) + str(node_client) + " and cost is {}".format(total_cost) 
    client_socket.send(message.encode())


def server(address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, PORT))
    server_socket.listen()
    clients = []
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        clients.append(client_address)
        
        if (len(clients) == len(IP) - 1):
            break
    server_socket.close()


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


def main():
    global addr_index
    if host_address == IP[addr_index]:
        server(IP[addr_index])
    else:
        client(IP[addr_index])
    
    addr_index += 1

    if (addr_index != len(IP)):
        main()

main()
    
