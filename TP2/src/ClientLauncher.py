import sys
from tkinter import Tk
from client import Client
import os

if __name__ == "__main__":
	try:
		serverAddr = sys.argv[1]
		serverPort = sys.argv[2]
		rtpPort = sys.argv[3]
		fileName = sys.argv[4]	
	except:
		print("[Usage: ClientLauncher.py Server_Addr Server_Port RTP_Port Video_file_Name]\n")	
	
	if os.environ.get('DISPLAY','') == '':
		print('no display found. Using :0.0')
		os.environ.__setitem__('DISPLAY', ':0.0')

	root = Tk()
	
	# Create a new client
	app = Client(root, serverAddr, serverPort, rtpPort, fileName)
	app.master.title("RTPClient")

	label1 = Tk.Label(app.master, text=f'Streaming {fileName}')
	label1.pack()
	
	root.mainloop()
	