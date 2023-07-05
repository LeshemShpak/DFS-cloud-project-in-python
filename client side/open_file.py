import sys
import os
import socket
import glob
import time
from cryptography.fernet import Fernet
PATH = r"C:\Users\user\Documents\my_doc"
SPLITTER_PRO = r'$$'
GET_FILE_NAME = 1
GET_IP = 2
GET_PORT = 3
CLIENT_REQUEST = r'client_request'
GET_FILE = r'get_file'
BUFFER = 1024
WRITE_BYTES = 'wb'
CLOSING = r'\\'
SEC_IN_HOUR = 3600
HOURS_TO_DEL = 12
KEY = b'vzh4IM34z_YVlig9f6jp_Y1hfoNpzsicito7wjcOI-Y='


def main():
    check_all_modules()
    try:
        for file in os.scandir(PATH):
            try:
                if hours_since_file_created(file.path) >= HOURS_TO_DEL:
                    os.remove(file.path)
            except OSError as e:
                print(e)
    except (OSError, NameError, AttributeError):
        print("cloud not scan the dir path:  " + PATH)
    # get parameters from the argv
    try:
        file_name = sys.argv[GET_FILE_NAME]
        ip = sys.argv[GET_IP]
        port = int(sys.argv[GET_PORT])
    except (OSError, NameError, AttributeError, IndexError):
        print("couldn't get parameters from argv")
        return
    recive_the_file(ip, port, file_name)

def  check_all_modules():
    try:
        os.getpid()
    except ModuleNotFoundError:
        print("you don't have os module, you need to download it")
    try:
        sys.argv
    except ModuleNotFoundError:
        print("you don't have sys module, you need to download it")
    try:
        time.time()
    except ModuleNotFoundError:
        print("you don't have time module, you need to download it")
    try:
        socket.socket()
    except ModuleNotFoundError:
        print("you don't have socket module, you need to download it")
    try:
        glob.magic_check()
    except ModuleNotFoundError:
        print("you don't have glob module, you need to download it")

def encrypt(mes):
    try:
        f = Fernet(KEY)
    except ModuleNotFoundError:
        print("you don't have Fernet module, you need to download it")
    f = Fernet(KEY)
    return f.encrypt(mes)


def decrypt(mes):
    try:
        f = Fernet(KEY)
    except ModuleNotFoundError:
        print("you don't have Fernet module, you need to download it")
    f = Fernet(KEY)
    return f.decrypt(mes)


def hours_since_file_created(filename):
    dt1 = os.path.getctime(filename)
    dt2 = time.time()
    delta = dt2 - dt1
    return delta / SEC_IN_HOUR


def recive_the_file (ip, port, file_name):
    try:
        # open communication
        client_socket = socket.socket()
        client_socket.connect((ip, port))
        # protocol structure: CLIENT_REQUEST + $$ + COMMAND + $$ + NAME_OF_THE_FILE
        client_socket.send(encrypt((CLIENT_REQUEST + SPLITTER_PRO + GET_FILE + SPLITTER_PRO + file_name).encode()))
        rec = decrypt(client_socket.recv(BUFFER))
        with open(PATH + CLOSING + file_name, WRITE_BYTES) as output:
            if rec:
                output.write(rec)
            while True:
                rec = decrypt(client_socket.recv(BUFFER))
                if not rec:
                    break
                output.write(rec)
        output.close()
    except (ConnectionRefusedError, ConnectionResetError, socket.error, OSError):
        print("did not wrote the file, os or communication problem")
        return
    try:
        os.startfile(PATH + CLOSING + file_name)
    except OSError:
        print("failed to open the file")
        return
    print('Success!')


if __name__ == '__main__':
    main()
