import socket
import threading

localIP = "127.0.0.1"
localPort = 20001
ADDR = (localIP, localPort)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Create a datagram socket
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
server.bind(ADDR)

print("UDP server up and listening")


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        print(f'[{addr}] sent {msg}')
    conn.close()


def start():
    print(f"[STARTING] server on {localPort} port.")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


start()
