import sys, socket
import threading
from ServerWorker import ServerWorker


def streamVideoAudio(rtspSocket):
	# Receive client info (address,port) through RTSP/TCP session
	while True:
		try:
			clientInfo = {}
			clientInfo['rtspSocket'] = rtspSocket.accept()  # clientInfo['rtspSocket'] = (clientConnection, clientAddress)
			ServerWorker(clientInfo).run()
		except Exception:
			break


def streamText():
	pass


if __name__ == "__main__":

	try:
		SERVER_PORT = int(sys.argv[1])
	except:
		print("[Usage: Server.py Port]\n")   

	SERVER_ADDR = "10.0.0.10"
	rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	rtspSocket.bind((SERVER_ADDR, SERVER_PORT))
	print(f"Listening on {SERVER_ADDR}: {SERVER_PORT}")
	rtspSocket.listen(5)

	# Receive client info (address,port) through RTSP/TCP session
	while True:
		try:
			clientInfo = {}
			clientInfo['rtspSocket'] = rtspSocket.accept()  # clientInfo['rtspSocket'] = (clientConnection, clientAddress)
			threading.Thread(target=ServerWorker(clientInfo).run, args=()).start() 
		except Exception:
			break

	rtspSocket.close()