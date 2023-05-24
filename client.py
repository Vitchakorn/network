import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_message = input("Message: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))


message = my_message.encode('utf-8')
client_socket.send(message)

while True:
    msg = client_socket.recv(1024)
    print(msg.decode("utf-8"))





