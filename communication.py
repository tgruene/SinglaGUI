import socket

class PyJEMClient:

    def __init__(self):
        self.s = socket.socket()
        self.host = "a526-hodgkin"#"172.17.41.22"
        self.port = 12344 #12345

    def run_code(self, query):
        try:
            self.s.send(query.encode())
            response = self.s.recv(1024)
            if len(response) == 0:
                return None
            else:
                return eval(response.decode())
        except:
            return None

    def connect(self):
        print("connecting to", self.host, self.port)
        self.s.connect((self.host, self.port))

    def disconnect(self):
        try:
            print("disconnecting")
            self.s.send(b"@quit")
            self.s.close()
        except:
            pass
