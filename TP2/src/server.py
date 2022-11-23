import socket
import threading

def main():
    server: socket.socket
    localIP: str
    localPort: int
    message: bytes
    localAddr: tuple
    addr: tuple

    localIP = "10.0.0.10"   # ver qual é a porta do servidor
    localPort = 3001
    localAddr = (localIP, localPort)
    """
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    """
    # Create a datagram socket
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    server.bind(localAddr)

    # Address and Port Available if print happens
    print(f'UDP server up and listening on {localIP}: {localPort}')

    # Catch the message - returns message and the device's (ip,port) that sent this message
    message, addr = server.recvfrom(1024)
    
    # Assure message was successfully received
    print(f"Message {message.decode('utf-8')} received from {addr}")

    # Send a response to the message received
    server.sendto("Success!!".encode('utf-8'), addr)

    # Close socket
    server.close()


if __name__ == '__main__':
    main()

"""
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
"""