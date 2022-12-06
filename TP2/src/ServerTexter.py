import sys, traceback, threading, socket

class ServerTexter:
	
	clientInfo = {}
	
	def __init__(self, clientInfo):
		self.clientInfo = clientInfo
		
	def run(self):
		threading.Thread(target=self.recvRtspRequest).start()
	
	def recvRtspRequest(self):
		connSocket = self.clientInfo['rtspSocket'][0]
        try:
            address = self.clientInfo['rtspSocket'][1][0]
            port = int(self.clientInfo['rtpPort'])
        except:
            print("Connection Error!!")
		while True:
			try:      
				message, addr = connSocket.recvfrom(1024)
				if message:
					print("Message received: \n" + data.decode("utf-8"))
					# self.processRtspRequest(data.decode("utf-8"))
                    connSocket.sendto(f"Sucess!!".encode('utf-8'), addr)
			except Exception:
				break