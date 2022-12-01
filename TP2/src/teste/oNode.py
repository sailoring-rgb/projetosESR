import json
from datetime import datetime, timedelta
import threading
from time import sleep
import sys

# ----------------------- oNode -----------------------

id = str(sys.argv)[0]

c = open(f'topologia{id}.json')
i = open(f'node_info{id}.json')

connections = json.load(c)
info = json.load(i)

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


def refresh(tabela, tempo_recebido, true_sender, n_saltos, timestamps, tree_back_to_sender, is_server, is_bigNode):
    nodo, tempo = timestamps[0]
    delta = tempo_recebido - tempo

    if true_sender in local_info_index:
        sender_index = local_info_index[true_sender]

        # tabela[index] = (nodo, tempo, last_refresh, is_server, is_bigNode, fastest_path)
        tabela[sender_index]['last_refresh'] = datetime.now()
        if tabela[sender_index]['tempo'] > delta:
            tabela[sender_index]['tempo'] = delta
            tabela[sender_index]['fastest_path'] = tree_back_to_sender

        elif tabela[sender_index]['tempo'] == delta & tabela[sender_index]['saltos'] >= n_saltos:
            tabela[sender_index]['tempo'] = delta
            tabela[sender_index]['fastest_path'] = tree_back_to_sender
            tabela[sender_index]['saltos'] = n_saltos
    else:
        n = len(local_info_index)
        local_info_index[true_sender] = n
        tabela[n] = {
            'nodo': true_sender,
            'tempo': delta,
            'saltos': n_saltos,
            'last_refresh': datetime.now(),
            'is_server': is_server,
            'is_bigNode': is_bigNode,
            'fastest_path': tree_back_to_sender
        }
    return tabela


def forward_mensagem(true_sender, n_saltos, timestamps, tree_back_to_sender, is_server, is_bigNode):
    timestamps.append(node_id, datetime.now())

    new_tree = [node_id, tree_back_to_sender]
    return true_sender, n_saltos + 1, timestamps, new_tree, is_server, is_bigNode


def message():
    # TODO enviar por UDP
    return node_id, 1, [(node_id, datetime.now())], [node_id], is_server, is_bigNode


def message_handler():
    # flooding controlado
    for i in local_info:
        delta = datetime.now() - i['last_refresh']
        expired = timedelta(minutes=1)
        if delta > expired:
            nodo = i['nodo']
            # TODO enviar por UDP
            message()
    pass


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


threads = []

media_player = threading.Thread(target=ui_handler, args=())
media_player.start()

servidor = threading.Thread(target=server_handler, args=())
servidor.start()

servidor.join()
media_player.join()
