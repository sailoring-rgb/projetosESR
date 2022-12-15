import socket
from socket import SO_REUSEADDR, SOL_SOCKET

from Streaming.ServerStreamer import ServerStreamer


def handler_404(client_info, is_big_node):
    if is_big_node:
        # envia um pedido ao servidor mais próximo
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


def stream(streamer_info):
    # streamer_info = (node_id, port_streaming, is_server, MAX_CONN, file_id)
    nodes_interested = []

    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    rtsp_socket.bind((streamer_info[0], streamer_info[1]))

    if streamer_info[2]:
        print(f"\nServidor à escuta em {streamer_info[0]}: {streamer_info[1]} (streaming)\n")
    else:
        print(f"\nBig Node à escuta em {streamer_info[0]}: {streamer_info[1]} (streaming)\n")

    rtsp_socket.listen(streamer_info[3])

    # Receber informação sobre cliente (ip,porta) através da sessão RTSP/TCP
    while True:

        client_info = {}
        try:
            client_info = {'rtspSocket': rtsp_socket.accept()}
            ServerStreamer(client_info, streamer_info[4], nodes_interested).run()

        except Exception as ex:
            if ex == "404":
                handler_404(client_info, not streamer_info[2])
            elif ex == "500":
                handler_500(client_info)
            else:
                print(f"Exception: [{ex}]\n")
            break

    rtsp_socket.close()