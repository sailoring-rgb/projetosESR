import json
from datetime import datetime, timedelta
import threading
from time import sleep
import sys
import socket

file_id = str(sys.argv)[0]

c = open(f'topologia{file_id}.json')
i = open(f'node_info{file_id}.json')

info = json.load(i)
connections = json.load(c)

node_id = info['node_id']
is_bigNode = info['is_bigNode']
is_server = info['is_server']

local_info_index = {}
local_info = []

for dados in info:
    n = len(local_info_index)
    local_info_index[dados['node_id']] = n
    local_info[n] = {
        'nodo': dados['node_id'],
        'tempo': 1,
        'saltos': len(dados['fastest_path']),
        'last_refresh': datetime.now(),
        'is_server': dados['is_server'],
        'is_bigNode': dados['is_bigNode'],
        'fastest_path': dados['fastest_path']
    }


def ui_handler():
    print('a iniciar client...')
    while (True):
        print('*doing client stuff*')
        sleep(2)


# m = {tempo_recebido, true_sender, n_saltos, timestamps, tree_back_to_sender, is_server, is_bigNode}
def refresh(tabela, m):
    nodo, tempo = m['timestamps'][0]
    delta = m['tempo_recebido'] - tempo

    if m['true_sender'] in local_info_index:
        sender_index = local_info_index[m['true_sender']]

        # tabela[index] = (nodo, tempo, last_refresh, is_server, is_bigNode, fastest_path)
        tabela[sender_index]['last_refresh'] = datetime.now()
        if tabela[sender_index]['tempo'] > delta:
            tabela[sender_index]['tempo'] = delta
            tabela[sender_index]['fastest_path'] = m['tree_back_to_sender']

        elif tabela[sender_index]['tempo'] == delta & tabela[sender_index]['saltos'] >= m['n_saltos']:
            tabela[sender_index]['tempo'] = delta
            tabela[sender_index]['fastest_path'] = m['tree_back_to_sender']
            tabela[sender_index]['saltos'] = m['n_saltos']
    else:
        n_ = len(local_info_index)
        local_info_index[m['true_sender']] = n_
        tabela[n_] = {
            'nodo': m['true_sender'],
            'tempo': delta,
            'saltos': m['n_saltos'],
            'last_refresh': datetime.now(),
            'is_server': is_server,
            'is_bigNode': is_bigNode,
            'fastest_path': m['tree_back_to_sender']
        }
    return tabela


def forward_mensagem(true_sender, n_saltos, timestamps, tree_back_to_sender, is_server, is_bigNode):
    timestamps.append(node_id, datetime.now())
    # TODO flooding controlado ver quem já recebeu
    new_tree = [node_id, tree_back_to_sender]
    return true_sender, n_saltos + 1, timestamps, new_tree, is_server, is_bigNode


def handler_answer(sock):
    done = False
    while not done:
        # receive incoming packets
        data, address = sock.recvfrom(4096)

        # print the received data and address
        print(f"Message {data.decode('utf-8')} received from {address}")
        done = True
    sock.close()


def message(ip, port):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    send_to = (ip, port)
    message_ = f'{node_id}, {1}, {[(node_id, datetime.now())]}, {[node_id]}, {is_server}, {is_bigNode}'

    sock.sendto(message_.encode('utf-8'), send_to)
    handler_answer(sock)


def message_worker(entry):
    delta = datetime.now() - entry['last_refresh']
    expired = timedelta(minutes=2)
    if delta > expired:
        nodo = entry['nodo']
        message(nodo, 5555)


def message_handler():
    messages_threads = []
    for entry in local_info:
        thread = threading.Thread(target=message_worker, args=(entry,))
        thread.start()
        messages_threads.append(thread)
    for thread in messages_threads:
        thread.join()


def network_handler():
    # recebe e passa informação

    # if is_bigNode : armazena tabela de ficheiros locais da sua subrede
    pass


def server_handler():
    print('a iniciar servidor servidor...')
    refresh_table = threading.Thread(target=message_handler, args=())
    refresh_table.start()

    network = threading.Thread(target=network_handler, args=())
    network.start()

    refresh_table.join()
    network.join()

# ----------------------- oNode.py -----------------------


threads = []

media_player = threading.Thread(target=ui_handler, args=())
media_player.start()

servidor = threading.Thread(target=server_handler, args=())
servidor.start()

servidor.join()
media_player.join()
