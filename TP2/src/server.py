import socket
import threading
import time
import database

def processMessage(server, message, addr, data):

    # Assure message was successfully received
    print(f"Message {message.decode('utf-8')} received from {addr}")

    data.addNeighbor(addr)

    # To guarantee that parallelism is happening
    time.sleep(6)

    # Send a response to the message received
    server.sendto("Success!!".encode('utf-8'), addr)


def processMessage2(server, message, addr, data):
    data.removeNeighbor(addr)
    server.sendto("Success!!".encode('utf-8'), addr)


def service(data, typeService: int):
    server: socket.socket
    localIP: str
    localPort: int
    message: bytes
    localAddr: tuple
    addr: tuple

    if typeService == 1:
        localPort = 3000
    elif typeService == 2:
        localPort = 3005
    else: # typeService == 3
        pass
    
    if typeService == 1 or 2:
        localIP = "10.0.0.10"   # ver qual é a porta do servidor
        localAddr = (localIP, localPort)

        # Create a datagram socket
        server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        server.bind(localAddr)

        # Address and Port Available if print happens
        print(f'UDP server up and listening on {localIP}: {localPort}')

        # To receive multiple messages:
        while True:

            try:
                # Catch the message - returns message and the device's (ip,port) that sent this message
                message, addr = server.recvfrom(1024)

                if typeService == 1:
                    threading.Thread(target=processMessage, args=(server,message,addr,data)).start()
                else: #typeService == 2
                    threading.Thread(target=processMessage2, args=(server,message,addr,data)).start()

            except socket.error:
                break

        # Close socket
        server.close()

    else: # typeService == 3
        while True:
            data.printNeighbors()


def main():

    data = database.database()

    # Multiple services, each one accepting multiple clients rather than one service accepting multiple clients
    # One socket listening at local port and another socket listening on another port to identify the wanted service

    # Responsible for adding data
    threading.Thread(target=service, args=(data,1,)).start()

    # Responsible for removing data
    threading.Thread(target=service, args=(data,2,)).start()

    # Responsible for printing data
    threading.Thread(target=service, args=(data,3,)).start()

    
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