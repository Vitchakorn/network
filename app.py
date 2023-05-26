import socket
import threading

PORT = 1234
IP = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
host_name = socket.gethostname()
host_address = socket.gethostbyname(host_name)
host_node = IP.index(host_address)
addr_index = 0 
total_cost = 0


# def handle_client():
    # message = "received node" + str(IP.index(host_address)) + " from " + host_address
    # client_socket.send(message.encode())
    # client_socket.close()
    

def server(address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, PORT))
    server_socket.listen()
    clients = 0 
    while True:
        client_socket, client_address = server_socket.accept()
        print("cli_address :" + client_address)
        print("cli_socket :" + client_socket)
        # client_thread = threading.Thread(
        #     target=handle_client, args=(client_socket))
        # client_thread.start()
        message = "received node" + str(IP.index(host_address)) + " from " + host_address
        client_socket.send(message.encode())
        client_socket.close()
        clients += 1
        if clients >= 3:
            break
    server_socket.close()

def client(address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, PORT))
    message = client_socket.recv(1024).encode('utf-8')
    print(message)
    client_socket.close()

def main():
    global addr_index
    if host_address == IP[host_node]:
        server(host_address)
    else:
        client(host_address)
    
    addr_index += 1

    if (addr_index != 4):
        main()

main()
    
