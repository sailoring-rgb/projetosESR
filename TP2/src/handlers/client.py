import os
import re
from tkinter import Tk
from time import sleep
from Streaming.ClientStreamer import ClientStreamer


def ui_handler(local_info, node_id, my_port, lock):
    print('A iniciar cliente...')

    local_info = {
        "nearest_server": [
            {"ip": "10.0.1.22",
            "port": "3010"}
        ]
    }
    while True:
        if os.environ.get('DISPLAY', '') == '':
            print('Nenhum display encontrado... Usar DISPLAY :0.0\n')
            os.environ.__setitem__('DISPLAY', ':0.0')

        current_pwd_path = os.path.dirname(os.path.abspath(__file__))
        video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
        filename = input(f'Introduza o nome do video: \n')
        path_to_filename = os.path.join(video_pwd_path, "play/" + str(filename))

        root = Tk()

        lock.acquire()
        
        # print("addr: " + str(local_info['nearest_server'][0][0]) + "\n" + "port: " + str(local_info['nearest_server'][0][1]))
        server_addr, server_port = local_info['nearest_server'][0]["ip"], int(local_info['nearest_server'][0]["port"])
        rtp_address, rtp_port = (node_id, my_port)
        lock.release()

        # Create a new client
        app = ClientStreamer(root, server_addr, server_port, rtp_address, rtp_port, path_to_filename)
        app.master.title("RTP Client")
        root.mainloop()
        sleep(2)