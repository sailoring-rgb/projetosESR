import os
import re
import sys
from tkinter import Tk

from ClientStreamer import ClientStreamer


def streamVideo(serverAddr: str, serverPort: int, rtpAddress: str, rtpPort: int):
	current_pwd_path = os.path.dirname(os.path.abspath(__file__))
	video_pwd_path = (re.findall("(?:(.*?)src)",current_pwd_path))[0]
	filename = input(f'Introduza o nome do video: \n')
	path_to_filename = os.path.join(video_pwd_path,"play/"+str(filename))

	root = Tk()
	# Create a new client
	app = ClientStreamer(root, serverAddr, serverPort, rtpAddress, rtpPort, path_to_filename)
	app.master.title("RTP Client")
	root.mainloop()


if __name__ == "__main__":
	try:
		serverAddr = sys.argv[1]  # server address
		serverPort = sys.argv[2]  # server port
		rtpAddress = sys.argv[3]  # client address
		rtpPort = sys.argv[4]     # client port
	except:
		print("[Usage: ClientLauncher.py Type_Stream Server_Addr Server_Port RTP_Port]\n")	
	
	if os.environ.get('DISPLAY', '') == '':
		print('No display found... Using DISPLAY :0.0\n')
		os.environ.__setitem__('DISPLAY', ':0.0')

	streamVideo(serverAddr,serverPort,rtpAddress,rtpPort)