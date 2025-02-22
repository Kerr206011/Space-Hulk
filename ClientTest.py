import socket
import threading

SERVER_HOST = '127.0.0.1'  # Change to the server's IP for Internet play
SERVER_PORT = 5000

def listen_to_server(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(f"Server: {data.decode()}")
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    threading.Thread(target=listen_to_server, args=(client,)).start()
    while True:
        msg = input("Enter message: ")
        if msg == "quit":
            break
        client.send(msg.encode())
    client.close()

start_client()