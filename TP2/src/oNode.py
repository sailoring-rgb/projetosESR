import datetime
import json
import os
import re
import socket
import struct
import sys
import threading
import time
import handlers.client as client
from Streaming.ServerStreamer import ServerStreamer

file_id = sys.argv[1]

current_pwd_path = os.path.dirname(os.path.abspath(__file__))
video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
path_to_topologia = os.path.join(video_pwd_path, "overlay/topologia" + str(file_id) + ".json")
path_to_node_info = os.path.join(video_pwd_path, "overlay/node_info" + str(file_id) + ".json")

c = open(path_to_topologia)
i = open(path_to_node_info)

info = json.load(i)
connections = json.load(c)

# ----------------------- variaveis locais -----------------------

node_id = info['node_id']
my_port = int(info['my_port'])
is_bigNode = info['is_bigNode']  # True / False
is_server = info['is_server']  # True / False
ports = info['ports']  # ({'ip': '192.168.1.3', 'port': 5000})

local_info = []  # mirrors message structure

# número max de saltos para o flooding
max_hops = 20

# número max de conexões
MAX_CONN = 25

# Estrutura da Mensagem a enviar aos nodos aquando do Flooding
message = {
    'nodo': node_id,
    'port': my_port,
    'tempo': [datetime.time()],
    'saltos': 0,
    'last_refresh': datetime.time(),
    'is_server': is_server,
    'is_bigNode': is_bigNode,
    'nearest_server': []
}

"""
Nesta Format String, o caractere > indica que os dados estão em big-endian byte order,
Os códigos de formatação individuais especificam os tipos dos campos em 'mensagem'.
O código de formatação '64s' indica que os campos 'nodo' e 'port' são strings de até 64 caracteres,
O código de formatação '16s' indica que os campos 'tempo' e 'last_refresh' são objetos de data e hora de até 16 chars
O código de formatação 'L' indica que o campo 'saltos' é um inteiro sem sinal de 32 bits,
O código de formatação '?' indica que os campos 'is_server' e 'is_bigNode' são booleanos,
O código de formatação '64s' no final indica que o campo 'nearest_server' é uma lista de strings de até 64 chars cada
"""

PACKET_FORMAT = ">64s64s16sL16s??64s"


# ----------------------- enviar mensagens -----------------------

def send_message(nodo, m):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"\n\n[{nodo['ip']}:{nodo['port']}] is sending a message \n{m}\n\n")
    s.bind((node_id, my_port))

    message_data = json.dumps(m)
    s.send(message_data)
    s.close()


def flood():
    for entry in ports:
        send_message(entry, message)


def refresh_message():
    message['tempo'] = [datetime.now()]
    message['last_refresh'] = datetime.now()


def refresh():
    flood()
    while True:
        time.sleep(30)
        refresh_message()
        flood()


# ----------------------- receber mensagens -----------------------

def check_and_register(m):
    if m['is_server'] or m['is_big_node']:
        delta = m['tempo'][1]

        if not message['nearest_server'] or (message['nearest_server'][0][1] >= (m['nearest_server'][0][1] + delta)
                                             or (message['nearest_server'][0][1] == m['nearest_server'][0][1]
                                                 + delta and m['saltos'] < message['saltos'])):
            message['nearest_server'] = [(m['nodo'], m['port'], m['tempo'][0] + delta)]


def receive_message(m):
    delta = datetime.now() - m['tempo'][0]
    m['tempo'][1] = delta

    if m['nodo'] == node_id:
        return

    if m['saltos'] >= max_hops:
        return

    # Se o nodo da mensagem já está na tabela local, atualiza
    if any(msg['nodo'] == m['nodo'] for msg in local_info):
        existing_message = next(msg for msg in local_info if msg['nodo'] == m['nodo'])
        existing_message.update(m)
        existing_message['last_refresh'] = datetime.time()
    else:
        m['saltos'] += 1
        m['last_refresh'] = datetime.time()
        local_info.append(m)

    # Verifica e Regista a informação do nodo na lista de servidores mais próximos
    check_and_register(m)

    flood()


def listening():
    s = socket.socket()
    s.bind((node_id, my_port))

    while True:
        data, address = s.recvfrom(1024)
        m0 = data.decode()

        packet_data = struct.unpack(PACKET_FORMAT, data)

        if 'nodo' not in packet_data:
            break

        m = json.loads(m0)
        receive_message(m)

    s.close()


def message_handler():
    time.sleep(60)
    rec = threading.Thread(target=listening, args=())
    send = threading.Thread(target=refresh, args=())

    rec.start()
    send.start()

    rec.join()
    send.join()


# ----------------------- envia ficheiros -----------------------

def handler_404(client_info):
    if is_bigNode:
        # verifica se tem ficheiros? se sim -> envia ficheiros, se não -> envia pedidos
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


def stream():
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.bind((node_id, my_port))

    if is_server:
        print(f"Servidor à escuta em {node_id}: {my_port}\n")
    if is_bigNode:
        print(f"Big Node à escuta em {node_id}: {my_port}\n")

    rtsp_socket.listen(MAX_CONN)

    # Receive client info (address,port) through RTSP/TCP session
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


# ----------------------- oNode.py -----------------------

lock = threading.Lock()

threads = []

refresh_table = threading.Thread(target=message_handler, args=())
refresh_table.start()

if is_server or is_bigNode:
    # escuta por pedidos e envia ficheiros
    streaming = threading.Thread(target=stream, args=())
    streaming.start()

if not is_server:
    # faz pedidos
    media_player = threading.Thread(target=client.ui_handler, args=(local_info, node_id, lock))
    media_player.start()


refresh_table.join()

if is_server or is_bigNode:
    streaming.join()

if not is_server:
    media_player.join()
