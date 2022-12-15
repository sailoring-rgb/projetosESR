from datetime import datetime, time, timedelta
import json
import os
import re
import socket
import sys
import threading
import time
import logging
from logging import FileHandler
from socket import SO_REUSEADDR, SOL_SOCKET

import handlers.oClient as Client
import handlers.oServer as Server

file_id = sys.argv[1]

current_pwd_path = os.path.dirname(os.path.abspath(__file__))
video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
path_to_node_info = os.path.join(video_pwd_path, "overlay/node_info" + str(file_id) + ".json")

i = open(path_to_node_info)

info = json.load(i)

# ----------------------- Logger -----------------------

# Create a FileHandler object
handler = FileHandler(f"{file_id}.txt")

# Create a Logger object and add the FileHandler
logger = logging.getLogger(f"{file_id}")
logger.addHandler(handler)

# Set the log level
logger.setLevel(logging.INFO)


# ----------------------- Variaveis locais -----------------------

node_id = info['node_id']
port_flooding = int(info['port_flooding'])
port_streaming = int(info['port_streaming'])
is_bigNode = bool(info['is_bigNode'])  # True / False
is_server = bool(info['is_server'])  # True / False
ports = info['ports']  # ({'ip': '192.168.1.3', 'port': 5000})

# Número max de saltos para o flooding
max_hops = 20

# Número max de conexões
MAX_CONN = 25

"""
Estrutura da Mensagem a enviar aos nodos aquando do Flooding:
{
    ip do nodo,
    porta para flooding
    porta para streaming
    (tempo de envio, delta de recepção da mensagem)
    número de saltos
    ultima atualização
    é Servidor?
    é Big Node?
    lista ordenada de servidores mais próximos:
        [(
            'ip', 'stream_port', 
            'ip interface de saída', 'stream_port interface de saída',
            tempo que demora a chegar a este servidor, 
            número de saltos, 
            é Servidor?
        )]
}
"""
message = {
    'nodo': node_id,
    'flood_port': port_flooding,
    'stream_port': port_streaming,
    'tempo': [datetime.now(), timedelta(days=0, hours=0, seconds=0)],
    'saltos': 0,
    'last_refresh': datetime.now(),
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

data_format = '%Y-%m-%d %H:%M:%S.%f'


# ----------------------- Enviar mensagens -----------------------

def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return str(obj)
    return json.JSONEncoder().default(obj)


def port_list_without(port):
    return [x for x in ports if x != port]


def port_list():
    return ports


def send_message(nodo, m, s):
    message_data = json.dumps(m, default=default)
    s.sendto(message_data.encode(), (nodo['ip'], int(nodo['port'])))


def flood(s, m, list_):
    for entry in list_:
        logger.info(f"\n[{node_id}] enviou para [{entry['ip']}:{entry['port']}]\n")
        send_message(entry, m, s)
    logger.info(f"a mensagem:\n{json.dumps(m, default=default, indent=4)}\n\n")


def refresh_message():
    logger.info(f"\n[{node_id}:{port_flooding}] is refreshing the flooding process.\n")
    message['tempo'][0] = datetime.now()
    message['last_refresh'] = datetime.now()


def refresh(s):
    flood(s, message, port_list())
    while True:
        logger.info(f"local info:\n{json.dumps(message['nearest_server'], default=default, indent=4)}\n\n")
        time.sleep(30)
        refresh_message()
        flood(s, message, port_list())


# ----------------------- Receber mensagens -----------------------

def convert_to_timedelta(data: str) -> timedelta:
    parts = data.split(":")
    days = int(parts[0].split(" ")[0])
    seconds = int(parts[1].split(" ")[0])

    delta = timedelta(days=days, seconds=seconds)
    return delta


def add_datetime_variable(list_, delta):
    result = []
    for ip, port, ip_is, port_is, date, s, b in list_:
        d = convert_to_timedelta(date)
        result.append((ip, port, ip_is, port_is, d + delta, s, b))
    return result


def merge_lists(l1, l2, m):
    new_list = []
    for i_ in range(len(l2)):
        new_tuple = (l2[i_][0], l2[i_][1], m['nodo'], m['stream_port'], l2[i_][4], l2[i_][5], l2[i_][6])
        new_list.append(new_tuple)

    merged_list = l1 + new_list
    sorted_list = sorted(merged_list, key=lambda x: (x[4], x[5]))
    return sorted_list


def filter_by_server(lst):
    result = []
    for tup in lst:
        if tup[6]:
            result.append(tup)
    return result


def check_and_register(m, delta_m):
    if is_server:
        return
    if is_bigNode:
        # procurar só servidores e manter-se a si como topo da lista
        lst = add_datetime_variable(m['nearest_server'], delta_m)
        merge = merge_lists(message['nearest_server'], filter_by_server(lst), m)
        message['nearest_server'] = merge
    elif not is_server and not is_bigNode:
        # procurar servidores ou bignodes e lista-los por proximidade
        lst = add_datetime_variable(m['nearest_server'], delta_m)
        message['nearest_server'] = merge_lists(message['nearest_server'], lst, m)


def receive_message(m, s):
    if m['nodo'] == node_id or is_server:
        return

    logger.info(f"[{node_id}:f{port_flooding}] recebeu: \n{json.dumps(m, default=default, indent=4)}.\n")

    tempo_str = m['tempo'][0]
    refresh_str = m['last_refresh']
    m['tempo'][0] = datetime.strptime(tempo_str.replace('T', ' '), data_format)
    m['last_refresh'] = datetime.strptime(refresh_str.replace('T', ' '), data_format)

    delta = datetime.now() - m['tempo'][0]
    m['tempo'][1] = delta

    if m['saltos'] >= max_hops:
        return

    check_and_register(m, delta)

    flood(s, m, port_list_without(m['flood_port']))


def listening(s):
    logger.info(f"[{node_id} à escuta em {port_flooding}]\n")

    while True:
        data, address = s.recvfrom(1024)

        # logger.info(f"[data]:\n[{data} from {address}]\n")

        m = json.loads(data)

        if 'nodo' not in m:
            break

        # logger.info(f"leu mensagem [{m}]")
        receive_message(m, s)

    s.close()


def message_handler():
    # time.sleep(10)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((node_id, port_flooding))

    if is_server or is_bigNode:
        t = timedelta(days=0, hours=0, seconds=0)
        if (node_id, port_streaming, node_id, port_streaming, t, 0, is_server) not in message['nearest_server']:
            message['nearest_server'].insert(0, (node_id, port_streaming, node_id, port_streaming, t, 0, is_server))

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

if is_server or is_bigNode:
    # Escuta por pedidos e envia ficheiros
    streaming = threading.Thread(target=Server.stream, args=(node_id, port_streaming, is_server, is_bigNode, MAX_CONN))
    streaming.start()

if not is_server:
    # Faz pedidos
    media_player = threading.Thread(target=Client.ui_handler, args=(message, node_id, port_streaming, lock))
    media_player.start()

refresh_table.join()

if is_server or is_bigNode:
    streaming.join()

else:
    media_player.join()
