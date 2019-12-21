from socket import *

class TCPClient:
    #HOST = '127.0.0.1'
    HOST = '192.168.1.108'
    PORT = 12345
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    
    def __init__(self):
        #self.client = socket(AF_INET, SOCK_STREAM)
        pass
        
    def connectToServer(self, address = ADDR):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.settimeout(5)
        self.client.connect(address)
    
    def disConnect(self):        
        try:
            self.client.close()
        except Exception as e:
            print (Exception, "Disconnect error:", e)
        
    def sendData(self, data):
        try:
            self.client.send(data)
        except Exception as e:
            print (Exception, "Send TCP Data error:", e)
    
    def recvData(self):
        try:
            return self.client.recv(self.BUFSIZ)
        except Exception as e:
            print (Exception, "Recv TCP Data error:", e)