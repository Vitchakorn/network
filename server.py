import socket
import select


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
addr_list = ['127.0.0.1', '127.0.0.2', '127.0.0.3', '127.0.0.4']

print(f'Listening for connections on {IP}:{PORT}...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
 
    except:
        return False

while True:
    client_socket, client_address = server_socket.accept()
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    message = receive_message(read_sockets)
    address = client_address[0]
    for target_node in range(len(addr_list)) :
            if addr_list[target_node] != address:
                client_socket.send(bytes(message + str(target_node+1) + '\n', 'utf-8'))
                
            # else:
            #     client_socket.send(bytes(address + "no path", 'utf-8'))



# while True:
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} has been established!")
#     clientsocket.send(bytes("send {} to 2 3 and 4".format(address), "utf-8"))


