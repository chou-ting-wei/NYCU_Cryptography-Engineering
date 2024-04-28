import socket
import threading
import time
import sys

# Create a socket object
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
VOTE_MESSAGE = "!VOTE"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    connected = True
    while connected:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            print(message)
        except ConnectionResetError:
            connected = False
    client.close()

def send():
    connected = True
    while connected:
        message = input()
        client.send(message.encode(FORMAT))
        if message == DISCONNECT_MESSAGE:
            connected = False
        elif message == VOTE_MESSAGE:
            id = input()
            vote = input()
            client.send(id.encode(FORMAT))
            client.send(vote.encode(FORMAT))
    client.close()

receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)
receive_thread.start()
send_thread.start()