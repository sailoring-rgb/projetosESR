import sys
from tkinter import Tk
from ClientWorker import ClientWorker
import os
import re

if __name__ == "__main__":
	current_pwd_path = os.path.dirname(os.path.abspath(__file__))
	video_pwd_path = (re.findall("(?:(.*?)src)",current_pwd_path))[0]
	try:
		serverAddr = sys.argv[1]
		serverPort = sys.argv[2]
		rtpAddress = sys.argv[3]
		rtpPort = sys.argv[4]
		fileName = os.path.join(video_pwd_path,"video/"+str(sys.argv[5]))
	except:
		print("[Usage: ClientLauncher.py Server_Addr Server_Port RTP_Port Video_file_Name]\n")	
	
	if os.environ.get('DISPLAY','') == '':
		print('No display found... Using DISPLAY :0.0')
		os.environ.__setitem__('DISPLAY', ':0.0')

	root = Tk()
	
	# Create a new client
	app = ClientWorker(root, serverAddr, serverPort, rtpAddress, rtpPort, fileName)
	app.master.title("RTPClient")

	root.mainloop()