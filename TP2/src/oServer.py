import datetime
import json
import os
import re
import socket
import struct
import sys
import threading
import time
import traceback
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