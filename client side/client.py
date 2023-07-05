# client
from multiprocessing import Process
from cryptography.fernet import Fernet
import sys
import myobserver
import time
import communication
import os
import win32com.client
import gui_cli
SERVER_IP = "192.168.1.30"
SERVER_PORT = 8080
CLIENT_PORT = 6060
USE_PATH_ICON = r'C:\Users\user\project_dfs\client\open_file.py '
TIME_SLEEP = 0.1
BUFFER = 1024
SPLITTER_PRO = r'$$'
SPLITTER_PATHS = r'%%'
SPLITTER_DATA = '####'
REGISTER_COMMAND = r'register'
REGISTER_USER_COMMAND = r'user_register'
CREATED_COMMAND = r'on_created'
DELETED_COMMAND = r'on_deleted'
MODIFIED_COMMAND = r"on_modified"
CHANGE_PATH_COMMAND = r'change_path'
TYPE_OF_REQUEST = 0
TYPE_OF_COMMAND = 1
NAME_OF_THE_FILE = 2
IP_OF_THE_CLIENT = 3
PORT_OF_THE_CLIENT = 4
SERVER_REQUEST = r'server_request'
CLIENT_REQUEST = r'client_request'
ICON = r'WScript.Shell'
SPACE = r' '
LINK = r'.lnk'
GET_FILE_CMD = r'get_file'
SLASH = r'\\'
READE_BYTES = r'rb'
FIRST_NAME = r'\coca cola'
SIZE_OF_FAILED_MESSAGES_2 = 2
FAILED_MES = 1
GET_ORG_PATH = 0
GET_NEW_PATH = 1
KEY = b'vzh4IM34z_YVlig9f6jp_Y1hfoNpzsicito7wjcOI-Y='


def main():
    print("very importent where you save 'open_file' on the computer")
    print("very importent where is your file creator folder")
    # create NetworkHandler object, to use with all the sends
    message_sender = communication.NetworkHandler(SERVER_IP, SERVER_PORT, CLIENT_PORT)
    screener = gui_cli.GUI(message_sender)
    try:
        screener.run()
    except ConnectionResetError:
        print("ConnectionResetError")
    path = screener.get_path()
    user_name = screener.get_user_name()
    password = screener.get_password()
    # create MyObserver object, if same changes occur in the path, send to server
    try:
        watcher = myobserver.MyObserver(path, user_name, password, message_sender)
        watcher.run()
    except ModuleNotFoundError:
        print("you don't have watchdog module, you need to download it")
    # listen to clients.
    message_sender.listen_clients_request(path)
    while True:
        try:
            time.sleep(TIME_SLEEP)
        except KeyboardInterrupt:
            watcher.stop()


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


def create_shortcut(path_icon, file_name, ip, port, path):
    print(path_icon)
    print(path)
    try:
        shell = win32com.client.Dispatch(ICON)
    except ModuleNotFoundError:
        print("you don't have win32com module, you need to download it")
    try:
        # desktop = r"path to where you wanna put your .lnk file"
        shell = win32com.client.Dispatch(ICON)
        shortcut = shell.CreateShortCut(path + FIRST_NAME + LINK)
        shortcut.Targetpath = sys.executable
        # shortcut.IconLocation = icon
        # go to the project in: use_path_icon - 'C:\Users\user\project_dfs\client\open_file.py '
        # then put in the arguments: 0 - file name   1 - ip   2 - port
        shortcut.Arguments = USE_PATH_ICON + file_name + SPACE + ip + SPACE + port
        # save the shortcut
        shortcut.save()
        os.rename(path + FIRST_NAME + LINK, path_icon)
    except (OSError, TypeError, TimeoutError):
        print("cloud not create an icon")


def handle_server_request(message, client_socket, address, path):
    print(message)
    # message structure: type_of_request  $$  type_of_command  $$  name_of_the_file  $$  ip  $$  port
    cmd = message[TYPE_OF_COMMAND]
    file_name = message[NAME_OF_THE_FILE]
    client_ip = message[IP_OF_THE_CLIENT]
    client_port = message[PORT_OF_THE_CLIENT]
    # r".lnk" - LINK: add to create the link
    # pull_path - where to create the icon, the shell of the data
    pull_path = path + file_name + LINK
    if cmd == CREATED_COMMAND:
        # the server sent message that this client need to create shell icon
        try:
            p2 = Process()
        except ModuleNotFoundError:
            print("you don't have multiprocessing module, you need to download it")
            return
        # open new process to create the shortcut_icon
        p1 = Process(target=create_shortcut, args=(pull_path, file_name, client_ip, client_port, path))
        p1.start()
        p1.join()
        print("creating an icon")
    if cmd == DELETED_COMMAND:
        # the server sent message that this client need to delete the icon, the owner client deleted is file
        print("deleting the file in this path: " + pull_path)
        try:
            os.remove(pull_path)
        except OSError:
            print("couldn't delete the file")
    if cmd == MODIFIED_COMMAND:
        # the sever sent message that this client need to change the name of the icon,
        # the owner client changed the name of the file
        paths = file_name.split(SPLITTER_PATHS)
        original_name = paths[GET_ORG_PATH]
        changed_name = paths[GET_NEW_PATH]
        print("change name of file, from:  "+original_name+"  to:  " + changed_name)
        os.rename(path+original_name + LINK, path+changed_name +LINK)


def handle_client_request(message, client_socket, path):
    # message structure: client_request  $$  type_of_command  $$  name of_the_file  $$  ip  $$  port
    cmd = message[TYPE_OF_COMMAND]
    file_name = message[NAME_OF_THE_FILE]
    # create full path
    pull_path = path + SLASH + file_name
    # for every command
    if cmd == GET_FILE_CMD:
        with open(pull_path, READE_BYTES) as file:
            while True:
                file_ch = file.read(BUFFER)
                while file_ch:
                    client_socket.send(file_ch)
                    file_ch = file.read(BUFFER)
                if not file_ch:
                    file.close()  # closing the file
                    client_socket.close()  # closing the socket
                    break  # get out of the loops


def handle_request(client_sock, address, path):
    message = decrypt(client_sock.recv(BUFFER)).decode()
    message = message.split(SPLITTER_PRO)
    # if len == 2, if the server send that it failed
    if len(message) == SIZE_OF_FAILED_MESSAGES_2:
        # the server notify about communication problems
        print(message[FAILED_MES])
    else:
        # message structure: type_of_request  $$  type_of_command  $$  name_of_the_file
        type_of_re = message[TYPE_OF_REQUEST]
        # if the message sent from the main server
        if SERVER_REQUEST == type_of_re:
            handle_server_request(message, client_sock, address, path)
        # if the message sent from the client
        if CLIENT_REQUEST == type_of_re:
            handle_client_request(message, client_sock, path)


if __name__ == '__main__':
    main()
