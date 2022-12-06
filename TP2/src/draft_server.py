import sys, socket, re
import threading
from ServerWorker import ServerWorker

class server:	
	
	def handle_type(type: str, clientInfo: dict){

		if re.match('[Aa][Cc][Kk]',type):
			pass # execute ack
		elif re.match('[Vv][Ii][Dd][Ee][Oo]|[Aa][Uu][Dd][Ii][Oo]',type):
			pass # execute ack
		elif re.match('[Tt][Ee][Xx][Tt]',type):
			rtspSocket.sendto("Sucess!! Message "+.encode('utf-8'), addr)
	}

	def main(self):
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
				# threading.Thread(target=ServerWorker(clientInfo).run, args=()).start()
				handle_type()
			except Exception:
				break

		rtspSocket.close()

if __name__ == "__main__":
	(server()).main()