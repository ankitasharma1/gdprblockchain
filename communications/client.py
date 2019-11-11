from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

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
                    if self.connect(self.host, self.port, True):
                        print("Reconnect successful, redoing last action")
                        return func(*args, **kw_args)
                else:
                    print("WARNING: Connection lost. New socket made. Try calling connect")
                    return
            except Exception as e:
                if type(e) == OSError or type(e) == IOError:
                    # OSError is raised when self.connect is what failed in the first place
                    # probably due to a timeout
                    pass
                else:
                    print(e)
                    print("ERROR: Unknown exception during failsafe process")
                return
    return wrapper

class Client():
    def __init__(self, timeout=5):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.connected = False
        self.retry = False
        self.host = None
        self.port = None
        self.timeout = timeout

    @failsafe
    def connect(self, host, port, retry=False):
        print(f"Connecting to {host} on port {port} ...")
        self.host = host
        self.port = port
        self.retry = retry
        while True:
            try:
                self.sock.connect((host, port))
                break
            except ConnectionRefusedError:
                if self.retry:
                    print(f"Connection refused by server {host}:{port} retrying in 5 seconds")
                    sleep(5)
                else:
                    print(f"Connection refused by server {host}:{port}")
                    return False
        self.connected = True
        print(f"Connected to {host} on port {port}")
        return True

    @failsafe
    def send(self, msg):
        self.sock.sendall(msg.encode('utf-8'))
        print("Message sent.")
        return True

    # TODO: replace msg_size default with global config variable MSG_SIZE
    @failsafe
    def recv(self, msg_size=1024):
        while True:
            data = self.sock.recv(msg_size)
            if data:
                return data

    def clean_up(self):
        self.sock.close()
        self.connected = False
        return True

if __name__ == '__main__':
    host = 'localhost'
    port = 50000
    c = Client()
    c.connect(host, port, True)
    c.send("hello")
    print(c.recv())
    c.clean_up()
    print("goodbye.")
