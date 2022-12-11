import threading
import socket
from src.Streaming.ServerStreamer import ServerStreamer


def server_handler(port, node_id, lock):
    print('A iniciar servidor...')
    lock.acquire()
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.bind((node_id, port))
    print(f"À escuta em {node_id}: {port}")
    lock.release()

    rtsp_socket.listen(5)

    # Receive client info (address,port) through RTSP/TCP session
    while True:
        try:
            clientInfo = {'rtspSocket': rtspSocket.accept()}
            ServerStreamer(client_info).run()
        except Exception:
            break
    # TODO
    # if is_bigNode : armazena tabela de ficheiros locais da sua subrede
    rtsp_socket.close()

"""
def network_handler(ports, node_id, lock):
    ports_threads = []

    for port in ports:
        lock.acquire()
        porta = int(port['port'])
        lock.release()
        thread = threading.Thread(target=port_handler, args=(porta,node_id,lock))
        thread.start()
        ports_threads.append(thread)
    for thread in ports_threads:
        thread.join()
    pass


def server_handler(port, node_id, lock):
    print('A iniciar servidor...')

    server = threading.Thread(target=port_handler, args=(port,node_id,lock))
    server.start()

    server.join()
"""