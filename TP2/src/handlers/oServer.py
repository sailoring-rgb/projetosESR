import socket
from socket import SO_REUSEADDR, SOL_SOCKET

from Streaming.ServerStreamer import ServerStreamer


def handler_404(client_info, is_big_node):
    if is_big_node:
        # Verifica se tem ficheiros? se sim -> envia ficheiros, se não -> envia pedidos
        pass
    else:
        print(f"404 NOT FOUND.\n{client_info}\n")
        reply = 'RTSP/1.0 404 NOT FOUND\nCSeq: ' + '\nSession: ' + str(client_info['session'])
        conn_socket = (client_info['rtspSocket'])[0]
        conn_socket.send(reply.encode())
    pass


def handler_500(client_info):
    print(f"500 CONNECTION ERROR.\n{client_info}\n")
    reply = 'RTSP/1.0 500 CONNECTION ERROR\nCSeq: ' + '\nSession: ' + str(client_info['session'])
    conn_socket = (client_info['rtspSocket'])[0]
    conn_socket.send(reply.encode())


def stream(node_id, my_port, is_server, is_big_node, max_conn):
    nodes_interested = []
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    rtsp_socket.bind((node_id, my_port))

    if is_server:
        print(f"\nServidor à escuta em {node_id}: {my_port} (streaming)\n")
    if is_big_node:
        print(f"\nBig Node à escuta em {node_id}: {my_port} (streaming)\n")

    rtsp_socket.listen(max_conn)

    # Receber informação sobre cliente (ip,porta) através da sessão RTSP/TCP
    while True:

        client_info = {}
        try:
            client_info = {'rtspSocket': rtsp_socket.accept()}
            nodes_interested.append(client_info)
            ServerStreamer(client_info,nodes_interested).run()
        except Exception as ex:
            if ex == "404":
                handler_404(client_info, is_big_node)
            elif ex == "500":
                handler_500(client_info)
            else:
                print(f"Exception: [{ex}]\n")
            break

    rtsp_socket.close()