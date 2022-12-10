import json
import datetime
import threading
import sys
import socket
import time
import struct
import os, re

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

# The message that will be sent to other nodes
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
O código de formatação 64s indica que os campos 'nodo' e 'port' são strings de até 64 caracteres,
O código de formatação 16s indica que os campos 'tempo' e 'last_refresh' são objetos de data e hora de até 16 caracteres
O código de formatação L indica que o campo 'saltos' é um inteiro sem sinal de 32 bits,
O ? código de formatação indica que os campos 'is_server' e 'is_bigNode' são booleanos,
O código de formatação 64s no final indica que o campo 'nearest_server' é uma lista de strings de até 64 caracteres cada
"""

PACKET_FORMAT = ">64s64s16sL16s??64s"


# ----------------------- enviar mensagens -----------------------

def send_message(nodo, m):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"\n\nPORTA: {int(nodo['port'])}\n\n")
    s.bind((nodo['ip'], int(nodo['port'])))

    # Serialize the message using JSON
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
            message['nearest_server'] = [(m['nodo'], m['tempo'][0] + delta)]


def receive_message(m):
    delta = datetime.now() - m['tempo'][0]
    m['tempo'][1] = delta

    if m['nodo'] == node_id:
        return

    if m['saltos'] >= max_hops:
        return

    # Se o nodo da mensagem já está na tabela local, atualiza
    if any(msg['nodo'] == m['nodo'] for msg in self.local_info):
        existing_message = next(msg for msg in self.local_info if msg['nodo'] == m['nodo'])
        existing_message.update(m)
        existing_message['last_refresh'] = datetime.time()
    else:
        m['saltos'] += 1
        m['last_refresh'] = datetime.time()
        self.local_info.append(m)

    # Verifica e Regista a informação do nodo na lista de servidores mais próximos
    check_and_register(m)

    flood()

def listen_to(nodo):
    s = socket.socket()
    s.bind((nodo['ip'], int(nodo['port'])))

    # Start listening for incoming connections
    s.listen(1)
    conn, addr = s.accept()

    while True:
        data = conn.recv(1024)
        m0 = data.decode()

        packet_data = struct.unpack(PACKET_FORMAT, data)

        if 'nodo' not in packet_data:
            break

        m = json.loads(m0)
        receive_message(m)

    conn.close()


def listening():
    for node in ports:
        t = threading.Thread(target=listen_to, args=(node,))
        t.start()


def message_handler():
    rec = threading.Thread(target=listening, args=())
    send = threading.Thread(target=refresh, args=())

    rec.start()
    send.start()

    rec.join()
    send.join()


# ----------------------- oNode.py -----------------------

lock = threading.Lock()

threads = []

# ------ CLIENTE -------

if is_server == "False":
    media_player = threading.Thread(target=client.ui_handler, args=(local_info, node_id, lock))
    media_player.start()
    media_player.join()

# ------ SERVIDOR ------

elif is_server == "True":
    # refresh_table = threading.Thread(target=message_handler, args=())
    # refresh_table.start()
    # refresh_table.join()
    
    print('A iniciar servidor...\n')
    rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtspSocket.bind((node_id, my_port))
    print(f"À escuta em {node_id}: {my_port}\n")
    rtspSocket.listen(5)

	# Receive client info (address,port) through RTSP/TCP session
    while True:
        try:
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept()  # clientInfo['rtspSocket'] = (clientConnection, clientAddress)
            ServerStreamer(clientInfo).run()
        except Exception:
            break

    rtspSocket.close()
