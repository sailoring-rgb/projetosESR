import socket

if __name__ == '__main__':
    server : socket.socket
    localIP : str
    localPort : int
    message : bytes
    add : tuple

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localIP = '10.0.0.10'
    localPort = 3000

    server.bind((localIP, localPort))

    print(f"UDP server up and listening on {localIP}:{localPort}")

    while True:
        try:
            messageFromClient, addr = server.recvfrom(2048)
            print(f"Message {messageFromClient.decode('utf-8')} received from {addr}")
            messageFromServer = input("Escreva a sua resposta:\n")
            server.sendto(messageFromServer.encode('utf-8'), addr)        
        except Exception:
            break

    server.close()