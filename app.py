import socket
import threading
import time 

PORT = 9000
IP = ['172.28.5.1', '172.28.5.2', '172.28.5.3', '172.28.5.4']
host = socket.gethostname()
host_address = socket.gethostbyname(host)
index = 0 
graph = [[0, 2, 3, 4], [10, 0, 4, 7], 
         [6, 1, 0, 8], [9, 12, 11, 0]]


def tsp(graph):
    n = len(graph)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1, 1 << n):
        for current in range(n):
            if mask & (1 << current) == 0:
                continue
            for prev in range(n):
                if mask & (1 << prev) == 0:
                    continue
                dp[mask][current] = min(dp[mask][current], dp[mask ^ (1 << current)][prev] + graph[prev][current])

    min_cost = float('inf')
    for i in range(1, n):
        cost = dp[(1 << n) - 1][i] + graph[i][0]
        if cost < min_cost:
            min_cost = cost
            
    return min_cost


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
    global total_cost
    node_host = IP.index(host_address)
    node_client = IP.index(client_address[0])
    cost = graph[node_host][node_client]
    message = str(node_client) + str(node_host) + " cost = {}".format(cost) 
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
    else :
        min_cost = tsp(graph)
        print("Minimum Cost:", min_cost)

main()
print(index)
    
