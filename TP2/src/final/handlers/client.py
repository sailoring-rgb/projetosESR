import os
import re
from tkinter import Tk
from src.final.Streaming.ClientStreamer import ClientStreamer
from time import sleep

from src.final.oNode import lock


def nearest_big_node(local_info):
    # TODO calculate nearest big Node
    return 0, 1


def ui_handler(local_info, node_id):
    print('a iniciar client...')
    while True:
        if os.environ.get('DISPLAY', '') == '':
            print('No display found... Using DISPLAY :0.0\n')
            os.environ.__setitem__('DISPLAY', ':0.0')

        current_pwd_path = os.path.dirname(os.path.abspath(__file__))
        video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
        filename = input(f'Introduza o nome do video: \n')
        path_to_filename = os.path.join(video_pwd_path, "play/" + str(filename))

        root = Tk()

        lock.acquire()
        server_addr, server_port = nearest_big_node(local_info)
        rtp_address, rtp_port = (node_id, server_port)
        lock.release()

        # Create a new client
        app = ClientStreamer(root, server_addr, server_port, rtp_address, rtp_port, path_to_filename)
        app.master.title("RTP Client")
        root.mainloop()
        sleep(2)