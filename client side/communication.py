import socket
import threading
from client import handle_request
from cryptography.fernet import Fernet
SPLITTER_PRO = r'$$'
IP_BASE = r'0.0.0.0'
ONE = 1
KEY = b'vzh4IM34z_YVlig9f6jp_Y1hfoNpzsicito7wjcOI-Y='
MODULE_MES_CRYPTOGRAPHY = "you don't have Fernet module, you need to download it"
MODULE_MES_THREADING = "check if if there is a problem with the server, timeout"
FAILED_TO_OPEN_COMMUNICATION = "failed to open communication"
TIME_OUT = "check if if there is a problem with the server, timeout"


def encrypt(mes):
    # get bits, return encrypted bits
    try:
        f = Fernet(KEY)
    except ModuleNotFoundError:
        print(MODULE_MES_CRYPTOGRAPHY)
    f = Fernet(KEY)
    return f.encrypt(mes)


def decrypt(mes):
    # get bits, return decrypted bits
    try:
        f = Fernet(KEY)
    except ModuleNotFoundError:
        print(MODULE_MES_CRYPTOGRAPHY)
    f = Fernet(KEY)
    return f.decrypt(mes)


class NetworkHandler:

    def __init__(self, ip, port, client_port):
        self.IP = ip
        self.PORT = port
        self.client_port = str(client_port)

    def send_message(self, message):
        try:
            # open socket
            client_socket = socket.socket()
            client_socket.connect((self.IP, self.PORT))
            client_socket.send(encrypt((message + SPLITTER_PRO + self.client_port).encode()))
            client_socket.close()
        except (ConnectionRefusedError, ConnectionResetError, socket.error):
            print(FAILED_TO_OPEN_COMMUNICATION)

    def send_and_rec(self, message):
        try:
            try:
                client_socket = socket.socket()
                client_socket.connect((self.IP, self.PORT))
                client_socket.send(encrypt((message + SPLITTER_PRO + self.client_port).encode()))
                ret_mes = (decrypt(client_socket.recv(1024))).decode()
                client_socket.close()
                return ret_mes
            except (ConnectionRefusedError, ConnectionResetError, socket.error):
                print(FAILED_TO_OPEN_COMMUNICATION)
        except TimeoutError:
            print(TIME_OUT)

    def listen_clients_request(self, path):
        server_sock = socket.socket()
        server_sock.bind((IP_BASE, int(self.client_port)))
        server_sock.listen(ONE)

        while True:
            # address - ip, port
            # establish communication
            client_sock, address = server_sock.accept()
            try:
                # using threads
                t1 = threading.Thread(target=handle_request, args=(client_sock, address, path))
                t1.start()
            except ModuleNotFoundError:
                print(MODULE_MES_THREADING)
