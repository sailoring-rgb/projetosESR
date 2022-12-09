import socket
import threading
import database


def processMessage(message, addr, server, data):
    data.addNeighbor(addr)
    server.sendto("Sucess!!".encode('utf-8'), addr)


def processMessage2(message, addr, server, data):
    data.removeNeighbor(addr)
    server.sendto("Sucess!!".encode('utf-8'), addr)


def service(data):
    server: socket.socket
    localIP: str
    localPort: int
    message: bytes
    add: tuple

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localIP = '10.0.0.10'
    localPort = 3000

    server.bind((localIP, localPort))

    print(f"UDP server up and listening on {localIP}:{localPort}")

    while True:
        try:
            message, add = server.recvfrom(1024)
            threading.Thread(target=processMessage, args=(message, add, server, data)).start()
        except Exception:
            break

    server.close()


def service2(data):
    server: socket.socket
    localIP: str
    localPort: int
    message: bytes
    addr: tuple

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localIP = '10.0.0.10'
    localPort = 3005

    server.bind((localIP, localPort))

    print(f"UDP server up and listening on {localIP}:{localPort}")

    while True:
        try:
            message, addr = server.recvfrom(1024)
            threading.Thread(target=processMessage2, args=(message, addr, server, data)).start()
        except Exception:
            break

    server.close()


def service3(data):
    while True:
        data.show()


def main():
    data: database.database

    data = database.database()
    threading.Thread(target=service, args=(data,)).start()
    threading.Thread(target=service2, args=(data,)).start()
    threading.Thread(target=service3, args=(data,)).start()


if __name__ == '__main__':
    main()
