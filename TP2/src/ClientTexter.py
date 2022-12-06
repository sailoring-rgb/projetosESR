from tkinter import *
import tkinter.messagebox as tkMessageBox
from PIL import Image, ImageTk
import socket, threading, sys, traceback, os
from RtpPacket import RtpPacket


class ClientTexter:

    # Initiation..
    def __init__(self, serveraddr, serverport, rtpaddress, rtpport):
        self.serverAddr = serveraddr
        self.serverPort = int(serverport)
        self.rtpAddress = rtpaddress
        self.rtpPort = int(rtpport)
        self.connectToServer()

    def connectToServer(self):
        self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.rtspSocket.connect((self.serverAddr, self.serverPort))
        except:
            tkMessageBox.showwarning('Falha na conexão!', 'Conexão a \'%s\' falhou!.' %self.serverAddr)

    def run(self):	

        self.destAddr = (self.serverAddr,self.serverPort)

        stop = True
        while stop:
            messageFromClient = input('Introduza a mensagem: \n')
            if re.match("$[Ee][Xx][Ii][Tt]|[Qq][Uu][Ii][Tt]|[Ss][Tt][Oo][Pp]$",messageFromClient):
                stop = False
            else:
                self.rtspSocket.sendto(messageFromClient.encode('utf-8'), destAddr)
                messageFromServer, addr = self.rtspSocket.recvfrom(2048)
                print(f"Mensagem {messageFromServer.decode('utf-8')} recebida do {addr}")
        self.rtspSocket.close()
