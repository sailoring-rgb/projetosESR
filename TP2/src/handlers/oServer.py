import os, re, socket, sys
from tkinter import Tk
from time import sleep
from Streaming.ServerStreamer import ServerStreamer


def handler_404(client_info):
    if is_bigNode:
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


def stream(node_id, my_port, is_server, is_bigNode, MAX_CONN):
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.bind((node_id, my_port))

    if is_server == "True":
        print(f"\nServidor à escuta em {node_id}: {my_port}\n")
    if is_bigNode == "True":
        print(f"\nBig Node à escuta em {node_id}: {my_port}\n")

    rtsp_socket.listen(MAX_CONN)

    # Receber informação sobre cliente (ip,porta) através da sessão RTSP/TCP
    while True:

        client_info = {}
        try:
            client_info = {'rtspSocket': rtsp_socket.accept()}
            ServerStreamer(client_info).run()
        except Exception as ex:
            if ex == "404":
                handler_404(client_info)
            elif ex == "500":
                handler_500(client_info)
            else:
                print(f"Exception: [{ex}]\n")
            break

    rtsp_socket.close()