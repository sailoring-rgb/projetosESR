import socket

def main():
    client: socket.socket
    destIP: str
    destPort: int
    destAddr: tuple
    messageFromClient: str
    addr: tuple

    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    destIP = '10.0.0.10'
    destPort = 3001
    destAddr = (destIP,destPort)
    messageFromClient = "Hello UDP Server"

    client.sendto(messageFromClient.encode('utf-8'), destAddr)
    
    messageFromServer, addr = client.recvfrom(1024)

    print(f"Message {messageFromServer.decode('utf-8')} received from {addr}")

    client.close()

if __name__ == '__main__':
    main()