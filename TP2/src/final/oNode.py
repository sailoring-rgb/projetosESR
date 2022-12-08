import json
from datetime import datetime, timedelta
import threading
from time import sleep
import os
import re
import sys
import socket
from tkinter import Tk
from ClientStreamer import ClientStreamer
from ServerStreamer import ServerStreamer

file_id = str(sys.argv)[0]

c = open(f'topologia{file_id}.json')
i = open(f'node_info{file_id}.json')

info = json.load(i)
connections = json.load(c)

node_id = info['node_id']
is_bigNode = info['is_bigNode']  # True / False
is_server = info['is_server']  # True / False
ports = info['ports']  # ("IP_A":"3000")

local_info_index = {}
local_info = []

# DONE
for data in info:
    n = len(local_info_index)
    local_info_index[data['node_id']] = n
    local_info[n] = {
        'nodo': data['node_id'],
        'tempo': 1,
        'saltos': len(data['fastest_path']),
        'last_refresh': datetime.now(),
        'is_server': data['is_server'],
        'is_bigNode': data['is_bigNode'],
        'fastest_path': data['fastest_path']
    }


def nearest_big_node():
    # TODO calculate nearest big Node
    pass


def ui_handler():
    print('A iniciar cliente...')
    while (True):
        if os.environ.get('DISPLAY', '') == '':
            print('Nenhum display encontrado... Usando DISPLAY :0.0\n')
            os.environ.__setitem__('DISPLAY', ':0.0')

        current_pwd_path = os.path.dirname(os.path.abspath(__file__))
        video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
        filename = input(f'Introduza o nome do video: \n')
        path_to_filename = os.path.join(video_pwd_path, "play/" + str(filename))

        root = Tk()

        server_addr, server_port = nearest_big_node()

        rtp_address, rtp_port = (node_id, server_port)

        # Create a new client
        app = ClientStreamer(root, server_addr, server_port, rtp_address, rtp_port, path_to_filename)
        app.master.title("RTP Client")
        root.mainloop()
        sleep(2)


def refresh(table, time_received, true_sender, num_hops, timestamps, tree_back_to_sender, is_server, is_bigNode):
    node, time = timestamps[0]
    delta = time_received - time

    if true_sender in local_info_index:
        sender_index = local_info_index[true_sender]

        # table[index] = (node, time, last_refresh, is_server, is_bigNode, fastest_path)
        table[sender_index]['last_refresh'] = datetime.now()
        if table[sender_index]['tempo'] > delta:
            table[sender_index]['tempo'] = delta
            table[sender_index]['fastest_path'] = tree_back_to_sender

        elif table[sender_index]['tempo'] == delta & table[sender_index]['saltos'] >= num_hops:
            table[sender_index]['tempo'] = delta
            table[sender_index]['fastest_path'] = tree_back_to_sender
            table[sender_index]['saltos'] = num_hops
    else:
        n = len(local_info_index)
        local_info_index[true_sender] = n
        table[n] = {
            'nodo': true_sender,
            'tempo': delta,
            'saltos': num_hops,
            'last_refresh': datetime.now(),
            'is_server': is_server,
            'is_bigNode': is_bigNode,
            'fastest_path': tree_back_to_sender
        }
    return table


def forward_message(true_sender, num_hops, timestamps, tree_back_to_sender, is_server, is_bigNode):
    timestamps.append(node_id, datetime.now())
    # TODO flooding controlado ver quem já recebeu
    new_tree = [node_id, tree_back_to_sender]
    return true_sender, num_hops + 1, timestamps, new_tree, is_server, is_bigNode


def handler_answer(sock):
    done = False
    while not done:
        # receive incoming packets
        dataRec, address = sock.recvfrom(4096)

        # print the received data and address
        print(f"A mensagem {dataRec.decode('utf-8')} foi recebida a partir de {address}")
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
        node = entry['nodo']
        message(node, 5555)


def message_handler():
    messages_threads = []
    for entry in local_info:
        thread = threading.Thread(target=message_worker, args=(entry,))
        thread.start()
        messages_threads.append(thread)
    for thread in messages_threads:
        thread.join()


def port_handler(port):
    rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rtsp_socket.bind((node_id, port))
    print(f"À escuta em {node_id}: {port}")
    rtsp_socket.listen(5)

    # Receive client info (address,port) through RTSP/TCP session
    while True:
        try:
            client_info = {'rtspSocket': rtsp_socket.accept()}
            ServerStreamer(client_info).run()
        except Exception:
            break
    # TODO
    # if is_bigNode : armazena tabela de ficheiros locais da sua subrede
    rtsp_socket.close()


def network_handler():
    ports_threads = []

    for port in ports:
        port_aux = port.get(1)
        thread = threading.Thread(target=port_handler, args=(port_aux,))
        thread.start()
        ports_threads.append(thread)
    for thread in ports_threads:
        thread.join()
    pass


def server_handler():
    print('A iniciar servidor...')
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

server = threading.Thread(target=server_handler, args=())
server.start()

server.join()
media_player.join()