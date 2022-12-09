import threading
import socket
from src.Streaming.ServerStreamer import ServerStreamer
from src.oNode import message_handler, lock


def port_handler(port, node_id):
    lock.acquire()
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.bind((node_id, port))
    print(f"Listening on {node_id}: {port}")
    lock.release()

    rtsp_socket.listen(5)

    # Receive client info (address,port) through RTSP/TCP session
    while True:
        try:
            client_info = {'rtspSocket': rtsp_socket.accept()}
            ServerStreamer(client_info).run()
        except Exception:
            break
    # TODO
    # if is_bigNode : armazena tabela de ficheiros locais da sua subrede
    rtsp_socket.close()


def network_handler(ports):
    ports_threads = []

    for port in ports:
        lock.acquire()
        porta = port['port']
        lock.release()
        thread = threading.Thread(target=port_handler, args=(porta,))
        thread.start()
        ports_threads.append(thread)
    for thread in ports_threads:
        thread.join()
    pass


def server_handler(ports, node_id):
    print('a iniciar servidor servidor...')
    refresh_table = threading.Thread(target=message_handler, args=())
    refresh_table.start()

    network = threading.Thread(target=network_handler, args=(ports, node_id))
    network.start()

    refresh_table.join()
    network.join()