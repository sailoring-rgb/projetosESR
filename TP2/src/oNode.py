import datetime
import json
import os
import re
import socket
import sys
import threading
import time
import handlers.oClient as client
import handlers.oServer as server

file_id = sys.argv[1]

current_pwd_path = os.path.dirname(os.path.abspath(__file__))
video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
path_to_node_info = os.path.join(video_pwd_path, "overlay/node_info" + str(file_id) + ".json")

i = open(path_to_node_info)

info = json.load(i)

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


def port_list_without(port):
    return [x for x in ports if x != port]


def port_list():
    return ports


def send_message(nodo, m, s):
    print(f"\n\n[{nodo['ip']}:f{nodo['port']}] enviou: \n{json.dumps(m, default=default, indent=4)}\n\n")

    message_data = json.dumps(m, default=default)
    s.sendto(message_data.encode(), (nodo['ip'], int(nodo['port'])))


def flood(s, m, list_):
    for entry in list_:
        send_message(entry, m, s)


def refresh_message():
    print(f"\n[{node_id}:{port_flooding}] is refreshing the flooding process.\n")
    message['tempo'].insert(0, datetime.datetime.now())
    message['last_refresh'] = datetime.datetime.now()


def refresh(s):
    flood(s, message, port_list())
    while True:
        print(f"local info:\n{json.dumps(local_info, default=default, indent=4)}\n\n")
        time.sleep(30)
        refresh_message()
        flood(s, message, port_list())


# ----------------------- Receber mensagens -----------------------

def add_datetime_variable(list_, delta):
    result = []
    for ip, port, date in list_:
        result.append((ip, port, date + delta))
    return result


def check_and_register(m, delta_m):
    # se M não tiver nada a acrescentar -> sai
    if not m['nearest_server'] or is_server:
        return
    # se for bignode: procura servidores mais próximos
    if is_bigNode:
        # se tiver uma lista já formada, verifica se m têm caminhos mais rápidos
        if message['nearest_server']:
            t = message['nearest_server'][0][2]
            t_m = m['nearest_server'][0][2]
            if (t >= t_m + delta_m
                    or (t >= t_m + delta_m and message['saltos'] > m['saltos'])):
                merged_list = message['nearest_server'] + (add_datetime_variable(m['nearest_server'], delta_m))
                sorted_list = sorted(merged_list, key=lambda x: x[2])
                message.update({'nearest_server': sorted_list})
        else:
            message.update({'nearest_server': add_datetime_variable(m['nearest_server'], delta_m)})
    # se for nodo: procura bignodes/servidores mais próximos
    else:
        # se tiver uma lista já formada, verifica se m têm caminhos mais rápidos
        if message['nearest_server']:
            t = message['nearest_server'][0][2]
            t_m = m['nearest_server'][0][2]
            if (t >= t_m + delta_m
                    or (t >= t_m + delta_m and message['saltos'] > m['saltos'])):
                merged_list = message['nearest_server'] + (add_datetime_variable(m['nearest_server'], delta_m))
                sorted_list = sorted(merged_list, key=lambda x: x[2])
                message.update({'nearest_server': sorted_list})
        else:
            message.update({'nearest_server': add_datetime_variable(m['nearest_server'], delta_m)})


def receive_message(m, s):
    print(f"[{node_id}:f{port_flooding}] recebeu: \n{json.dumps(m, default=default, indent=4)}.\n")

    if m['nodo'] == node_id:
        return

    tempo_str = m['tempo'][0]
    refresh_str = m['last_refresh']
    m['tempo'][0] = datetime.datetime.strptime(tempo_str.replace('T', ' '), '%Y-%m-%d %H:%M:%S.%f')
    m['last_refresh'] = datetime.datetime.strptime(refresh_str.replace('T', ' '), '%Y-%m-%d %H:%M:%S.%f')

    delta = datetime.datetime.now() - m['tempo'][0]
    m['tempo'].insert(1, delta)

    # Se o nodo da mensagem já está na tabela local, atualiza
    if any(msg['nodo'] == m['nodo'] for msg in local_info):
        existing_message = next(msg for msg in local_info if msg['nodo'] == m['nodo'])
        existing_message.update(m)
        existing_message['last_refresh'] = datetime.time()
    else:
        m['saltos'] += 1
        m['last_refresh'] = datetime.time()
        local_info.append(m)

    if m['saltos'] >= max_hops:
        return

    check_and_register(m, delta)

    flood(s, m, port_list_without(m['flood_port']))


def listening(s):
    print(f"[{node_id} à escuta em {port_flooding}]\n")

    while True:
        data, address = s.recvfrom(1024)

        # print(f"[data]:\n[{data} from {address}]\n")

        m = json.loads(data)

        if 'nodo' not in m:
            break

        # print(f"leu mensagem [{m}]")
        receive_message(m, s)

    s.close()


def message_handler():
    time.sleep(10)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((node_id, port_flooding))

    if is_server:
        if (node_id, port_streaming, 0) not in message['nearest_server']:
            message['nearest_server'].insert(0, (node_id, port_streaming, 0))

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
