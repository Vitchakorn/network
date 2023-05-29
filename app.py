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
    last_city = -1
    for i in range(1, n):
        cost = dp[(1 << n) - 1][i] + graph[i][0]
        if cost < min_cost:
            min_cost = cost
            last_city = i
            
    path = [0]
    mask = (1 << n) - 1
    while last_city != 0:
        path.append(last_city)
        mask ^= (1 << last_city)
        for prev in range(n):
            if mask & (1 << prev) == 0:
                continue
            if dp[mask][last_city] == dp[mask ^ (1 << last_city)][prev] + graph[prev][last_city]:
                last_city = prev
                break
    path.append(0)

    return path, min_cost


def sending(server, address):
    node_host = IP.index(host_address)
    node_client = IP.index(address[0])
    cost = graph[node_host][node_client]
    message = str(node_client) + str(node_host) + " cost = {} ".format(cost) + str(address[0]) + str(host_address)
    server.send(message.encode())


def server(address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, PORT))
    server_socket.listen()
    clients = 0
    while True:
        server , address = server_socket.accept()
        time.sleep(1)
        client_thread = threading.Thread(
            target=sending, args=(server, address))
        client_thread.start()
        clients += 1

        if (clients == len(IP) - 1):
            break
    server_socket.close()


def main():
    global index
    print(index)
    if host_address == IP[index]:
        server(IP[index])
    else:
        client(IP[index])
    index += 1

    if (index != len(IP)):
        main()
    else :
        path, min_cost = tsp(graph)
        print("path:", path)
        print("Minimum Cost:", min_cost)

main()
    
