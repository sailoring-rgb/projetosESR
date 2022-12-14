import os
import re
from tkinter import Tk
from time import sleep
from Streaming.ClientStreamer import ClientStreamer


def ui_handler(local_info, node_id, my_port, lock):
    print('\nA iniciar cliente...')

    on = True
    
    while on:
        
        if os.environ.get('DISPLAY', '') == '':
            print('Nenhum display encontrado... Usar DISPLAY :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        current_pwd_path = os.path.dirname(os.path.abspath(__file__))
        video_pwd_path = (re.findall("(?:(.*?)src)", current_pwd_path))[0]
        # filename = input(f'\n\nIntroduza o nome do video: \n')
        filename = "movie.Mjpeg"

        # print("local_info: " + str(local_info))
        # if re.search(r"\:q", filename):
        #    on = False
        #else:
        path_to_filename = os.path.join(video_pwd_path, "play/" + str(filename))

        root = Tk()

        lock.acquire()

        # print("addr: " + str(local_info['nearest_server'][0][0]) + "\n" + "port: " + str(local_info['nearest_server'][0][1]))
        server_addr, server_port = local_info['nearest_server'][0][0], int(local_info['nearest_server'][0][1])
        rtp_address, rtp_port = (node_id, my_port)
        lock.release()

        # Create a new client
        app = ClientStreamer(root, server_addr, server_port, rtp_address, rtp_port, path_to_filename)
        app.master.title("RTP Client")
        root.mainloop()
        sleep(2)