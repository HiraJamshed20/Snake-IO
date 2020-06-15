import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '10.130.7.146'
        self.port = 8083
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def getpos(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2000).decode('ascii')
        except:
            pass

    def send(self, data):
        try:
            #print('Sending', data)
            self.client.sendall(data.encode('ascii'))
            return self.client.recv(1024).decode('ascii')
        except:
            return 0
            print(socket.error)

    def simplesend(self, data):
        self.client.sendall(data.encode('ascii'))

    def simplercv(self):
        try:
            return self.client.recv(1024).decode('ascii')
        except:
            return 0


