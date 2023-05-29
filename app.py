import socket
import threading
import time 
from itertools import permutations

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


def calculate_total_distance(path, graph):
    total_distance = 0
    num_cities = len(path)
    for i in range(num_cities - 1):
        source = path[i]
        destination = path[i+1]
        total_distance += graph[source][destination]
    # Add the distance from the last city back to the starting city
    total_distance += graph[path[num_cities - 1]][path[0]]
    return total_distance


def tsp(graph):
    num_cities = len(graph)
    # Generate all possible permutations of cities
    all_paths = permutations(range(num_cities))
    min_distance = float('inf')
    optimal_path = None
    for path in all_paths:
        distance = calculate_total_distance(path, graph)
        if distance < min_distance:
            min_distance = distance
            optimal_path = path
    return optimal_path, min_distance


def sending(server, address):
    node_host = IP.index(host_address)
    node_client = IP.index(address[0])
    cost = graph[node_host][node_client]
    message = str(node_client) + str(node_host) + " cost = {} ".format(cost)
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
    
