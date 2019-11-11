from socket import socket, AF_INET, SOCK_STREAM, timeout
from time import time, sleep

def failsafe(func):
    def wrapper(*args, **kw_args):
        try:
            return func(*args, **kw_args)
        except Exception as e:
            print(e)
            self = args[0]
            try:
                self.sock.close()
                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.settimeout(self.timeout)
                self.connected = False
                if self.retry:
                    print("Retry enabled. Starting reconnection ...")
                    if self.connect(True):
                        print("Reconnect successful, redoing last action")
                        return func(*args, **kw_args)
                else:
                    print("WARNING: Connection lost. New socket made. Try calling connect")
                    return
            except Exception as e:
                if type(e) == OSError:
                    # OSError is raised when self.connect is what failed in the first place
                    # probably due to a timeout
                    pass
                else:
                    print(e)
                    print("ERROR: Unknown exception during failsafe process")
                return
    return wrapper

class Server():
    def __init__(self, host, port, timeout=5):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.timeout = timeout
        self.connected = False
        self.host = host
        self.port = port
        self.client_addr = None
        self.client_conn = None
        self.retry = False
    
        self.sock.settimeout(timeout)

    @failsafe
    def connect(self, retry=False):
        self.retry = retry
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"Listening on {self.host}:{self.port} ...")
        self.client_conn, self.client_addr = self.sock.accept()
        self.connected = True
        print(f"Connected to {self.client_addr}")
        return True

    @failsafe
    def send(self, msg):
        self.client_conn.sendall(msg.encode('utf-8'))
        print("Message sent.")
        return True

    # TODO: replace msg_size default with global config variable MSG_SIZE
    @failsafe
    def recv(self, msg_size=1024):
        while True:
            data = self.client_conn.recv(msg_size)
            if data:
                return data

    def clean_up(self):
        self.sock.close()
        self.connected = False
        return True

if __name__ == '__main__':
    host = 'localhost'
    port = 50000
    s = Server(host, port)
    s.connect(True)
    print(s.recv())
    s.send("Goodday sir")
    s.clean_up()
    print("goodbye.")
