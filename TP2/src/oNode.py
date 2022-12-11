import datetime
import json
import os
import re
import socket
import struct
import sys
import threading
import time
import handlers.oClient as client
import handlers.oServer as server

file_id = sys.argv[1]

current_pwd_path = os.path.dirname(os.path.abspath(__file__))
video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
path_to_topologia = os.path.join(video_pwd_path, "overlay/topologia" + str(file_id) + ".json")
path_to_node_info = os.path.join(video_pwd_path, "overlay/node_info" + str(file_id) + ".json")

c = open(path_to_topologia)
i = open(path_to_node_info)

info = json.load(i)
connections = json.load(c)

# ----------------------- Variaveis locais -----------------------

node_id = info['node_id']
port_flooding = int(info['port_flooding'])
port_streaming = int(info['port_streaming'])
is_bigNode = info['is_bigNode']  # True / False
is_server = info['is_server']  # True / False
ports = info['ports']  # ({'ip': '192.168.1.3', 'port': 5000})

local_info = []  # mirrors message structure

# Número max de saltos para o flooding
max_hops = 20

# Número max de conexões
MAX_CONN = 25

# Estrutura da Mensagem a enviar aos nodos aquando do Flooding
message = {
    'nodo': node_id,
    'flood_port': port_flooding,
    'stream_port': port_streaming,
    'tempo': [datetime.datetime.now()],
    'saltos': 0,
    'last_refresh': datetime.datetime.now(),
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

PACKET_FORMAT = ">64s64s64s16sL16s??64s"


# ----------------------- Enviar mensagens -----------------------

def default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, datetime.time):
        return obj.strftime("%H:%M:%S")
    return json.JSONEncoder().default(obj)


def send_message(nodo, m, s):
    print(f"\n\n[{nodo['ip']}: {nodo['port']}] is sending a message \n{m}\n\n")

    message_data = json.dumps(m, default=default)
    s.sendto(message_data.encode(), (nodo['ip'], int(nodo['port'])))
    s.close()


def flood(s):
    for entry in ports:
        send_message(entry, message, s)


def refresh_message():
    print(f"\n[{node_id}:{port_flooding}] is refreshing the flooding process.\n")
    message['tempo'].insert(0, datetime.datetime.now())
    message['last_refresh'] = datetime.datetime.now()


def refresh(s):
    flood(s)
    while True:
        time.sleep(30)
        refresh_message()
        flood(s)


# ----------------------- Receber mensagens -----------------------

def check_and_register(m):
    if is_server:
        message['nearest_server'].insert(0, (node_id, port_flooding, 0))
        return
    if m['is_server'] == "True" or m['is_big_node'] == "True":
        delta = m['tempo'][1]

        if message['nearest_server'] != [] or (message['nearest_server'][0][2] >= (m['nearest_server'][0][2] + delta)
                                               or (message['nearest_server'][0][2] == m['nearest_server'][0][2]
                                                   + delta and m['saltos'] < message['saltos'])):
            message['nearest_server'].insert(0, (m['nodo'], m['stream_port'], m['tempo'][0] + delta))
        else:
            message['nearest_server'].append((m['nodo'], m['stream_port'], m['tempo'][0] + delta))


def receive_message(m, s):
    print(f"[{node_id}: {port_flooding}] recebeu: \n{m}.\n")

    delta = datetime.datetime.now() - m['tempo'][0]
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

    flood(s)


def listening(s):
    print(f"[{node_id} à escuta em {port_flooding}]\n")

    while True:
        data, address = s.recvfrom(1024)
        m0 = data.decode()

        print(f"[data]:\n[{data} from {address}]\n")

        node, port_f, port_s, timestamp, s, last_refresh, is_s, is_bn, nearest_s = struct.unpack(PACKET_FORMAT, data)

        m1 = {
            'nodo': node,
            'flood_port': port_f,
            'stream_port': port_s,
            'tempo': timestamp,
            'saltos': s,
            'last_refresh': last_refresh,
            'is_server': is_s,
            'is_bigNode': is_bn,
            'nearest_server': nearest_s
        }

        if 'nodo' not in m1:
            break

        print(f"leu mensagem [{m1}] -> m1")
        m = json.loads(m0)
        receive_message(m, s)

    s.close()


def message_handler():
    time.sleep(30)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((node_id, port_flooding))

    send = threading.Thread(target=refresh, args=(s,))
    rec = threading.Thread(target=listening, args=(s,))

    rec.start()
    send.start()

    rec.join()
    send.join()


# ----------------------- oNode.py -----------------------

lock = threading.Lock()

threads = []

refresh_table = threading.Thread(target=message_handler, args=())
refresh_table.start()

if is_server == "True" or is_bigNode == "True":
    # Escuta por pedidos e envia ficheiros
    streaming = threading.Thread(target=server.stream, args=(node_id, port_streaming, is_server, is_bigNode, MAX_CONN))
    streaming.start()

else:
    # Faz pedidos
    media_player = threading.Thread(target=client.ui_handler, args=(local_info, node_id, port_streaming, lock))
    media_player.start()

refresh_table.join()

if is_server == "True" or is_bigNode == "True":
    streaming.join()

else:
    media_player.join()
