import socket
import threading
import config

class MindwaveConnector(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.listen = True

    def run(self):
        self.sock.connect(self.server_address)
        if sock:
            self.sock.send(config.CONFSTRING.encode('utf8'))
        while self.listen:
            data = sock.recv(1024)
            dataform = data.decode()
            print(dataform)
            try:
                struct = json.loads(dataform)
                if struct and (('status' in struct and struct['status'] != "scanning") or 'status' not in struct):
                    #TODO store reading here
                    pass
            except Exception as e:
                print(str(e))