import sys, re, os, socket
from tkinter import Tk
from ClientStreamer import ClientStreamer
from ClientTexter import ClientTexter


def streamVideoAudio(typeStream: str, serverAddr: str, serverPort: int, rtpAddress: str, rtpPort: int):
	current_pwd_path = os.path.dirname(os.path.abspath(__file__))
	video_pwd_path = (re.findall("(?:(.*?)src)",current_pwd_path))[0]
	filename = input(f'Introduza o nome do {typeStream}: \n')
	path_to_filename = os.path.join(video_pwd_path,"content/"+str(filename))

	root = Tk()
	# Create a new client
	app = ClientStreamer(root, serverAddr, serverPort, rtpAddress, rtpPort, path_to_filename)
	app.master.title("RTP Client")
	root.mainloop()


def streamText(serverAddr: str, serverPort: int, rtpAddress: str, rtpPort: int):
	ClientTexter(serverAddr,serverPort,rtpAddress,rtpPort).run()


if __name__ == "__main__":
	try:
		typeStream = sys.argv[1]  # type of streaming (text | video | audio | ack)
		serverAddr = sys.argv[2]  # server address
		serverPort = sys.argv[3]  # server port
		rtpAddress = sys.argv[4]  # client address
		rtpPort = sys.argv[5]     # client port
	except:
		print("[Usage: ClientLauncher.py Type_Stream Server_Addr Server_Port RTP_Port]\n")	
	
	if os.environ.get('DISPLAY','') == '':
		print('No display found... Using DISPLAY :0.0\n')
		os.environ.__setitem__('DISPLAY', ':0.0')

	# Send to Server the Type of Stream
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	destAddr = (serverAddr,int(serverPort))
	client.sendto(typeStream.encode('utf-8'), destAddr)
	# client.listen(5)
	client.close()

	# Request Stream Video Or Audio
	if re.match("[Vv][Ii][Dd][Ee][Oo]|[Aa][Uu][Dd][Ii][Oo]", typeStream):
		streamVideoAudio(typeStream,serverAddr,serverPort,rtpAddress,rtpPort)

	# Request Stream Message
	elif re.match("[Tt][Ee][Xx][Tt]",typeStream):
		streamText(serverAddr,serverPort,rtpAddress,rtpPort)
	
	else:
		print("ERROR: O tipo de stream introduzido não é válido!")