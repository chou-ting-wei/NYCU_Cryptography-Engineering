import socket
import threading
import time
import sys

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
VOTE_MESSAGE = "!VOTE"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
clients_voting = {}


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            message = conn.recv(HEADER).decode(FORMAT)
            if message:
                print(f"[{addr}] {message}")
            if message == VOTE_MESSAGE:
                print(f"[{addr}] {message}")
                id = conn.recv(HEADER).decode(FORMAT)
                vote = conn.recv(HEADER).decode(FORMAT)
                if not vote:
                    print(f"[DISCONNECT] {addr} disconnected.")
                    connected = False
                    clients.remove(conn)
                    break
                if not ZKP(id, vote):
                    print(f"[ZKP] {addr} failed ZKP.")
                    continue
                if vote in clients_voting:
                    clients_voting[vote] += 1
                else:
                    clients_voting[vote] = 1
                print(f"[{addr}] Voted for {vote}")
                print(f"[VOTES] {clients_voting}")
                broadcast(f"[VOTES] {clients_voting}")
            elif message == DISCONNECT_MESSAGE:
                print(f"[DISCONNECT] {addr} disconnected.")
                connected = False
                clients.remove(conn)
            elif not message:
                print(f"[DISCONNECT] {addr} disconnected.")
                connected = False
                clients.remove(conn)
        except ConnectionResetError:
            print(f"[DISCONNECT] {addr} disconnected.")
            connected = False
            clients.remove(conn)
    conn.close()

def ZKP(ID, vote):
    return 1 #Validating id whithout knowing the who is the voter(Not implemented yet)

def broadcast(message):
    for client in clients:
        client.send(message.encode(FORMAT))

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] Server is starting...")
start()


