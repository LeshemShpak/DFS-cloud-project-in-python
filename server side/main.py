# server
import os
import socket
import threading
import xml.etree.ElementTree as Et
from cryptography.fernet import Fernet
OPEN_MESSAGE = r'open communication'
IP = '0.0.0.0'
IP_SUB_TAG = r'ip'
PATH_SUB_TAG = r'path'
CLIENTS_SUB_TAG = r'clients'
CLIENT_SUB_TAG = r'client'
FILES_SUB_TAG = r'files'
FILE_SUB_TAG = r'file'
PORT_SUB_TAG = r'port'
PASSWORD_SUB_TAG = r'password'
USER_NAME_SUB_TAG = r'user_name'
USER_SUB_TAG = 'user'
SPLITTER_PRO = r'$$'
SPLITTER_PATHS = r'%%'
SPLITTER_DATA = '####'
SERVER_REQUEST = r'server_request'
XML_SCRIPT_NAME = r'users.xml'
USE_HEBREW = r"utf-8"
REGISTER_COMMAND = r'register'
CREATED_COMMAND = r'on_created'
DELETED_COMMAND = r'on_deleted'
MODIFIED_COMMAND = r"on_modified"
CHANGE_PATH_COMMAND = r'change_path'
CHECK_USER_COMMAND = r'check_user'
CHANGE_NAME = r'on_moved'
REGISTER_USER_COMMAND = r'user_register'
CHANGE_ALL = "change_all_cmd"
GET_MY_PATH_COMMAND = r'get_path'
SPACE = r' '
GO_TO_IP = 0
GO_CMD = 0
GO_PATH = 1
GO_CLIENT_PORT = 2
GET_NAME_OF_FILE = -1
GET_FILE_NAME = 0
GET_IP = 1
GET_PORT = 2
GET_USER_NAME_FROM_MESSAGE = 0
GET_PASSWORD_FROM_MESSAGE = 1
GET_DATA_FROM_MESSAGE = 2
PORT = 8080
BUFFER_SIZE = 1024
clients = {}
POS_XML_DECLARATION = True
KEY = b'vzh4IM34z_YVlig9f6jp_Y1hfoNpzsicito7wjcOI-Y='


def main():
    # open socket
    print(OPEN_MESSAGE)
    try:
        server_sock = socket.socket()
    except ModuleNotFoundError:
        print("you do not have socket module, you have to download")
    try:
        server_sock = socket.socket()
        server_sock.bind((IP, PORT))
        server_sock.listen(1)
    except (ConnectionRefusedError, ConnectionResetError, socket.error):
        print("failed to open communication, socket error, can't run the program")
        return
    try:
        lock = threading.Lock()
    except ModuleNotFoundError:
        print("you do not have thread module, you have to download")

    while True:
        # address - ip, port
        # establish communication
        client_sock, address = server_sock.accept()
        # using threads
        try:
            lock = threading.Lock()
            t1 = threading.Thread(target=handle_client, args=(client_sock, address, lock))
            # start the thread
            t1.start()
        except ModuleNotFoundError:
            print("need to download module")


def encrypt(mes):
    try:
        f = Fernet(KEY)
    except ModuleNotFoundError:
        print("you don't have Fernet module, you need to download it")
    return f.encrypt(mes)


def decrypt(mes):
    try:
        f = Fernet(KEY)
    except ModuleNotFoundError:
        print("you don't have Fernet module, you need to download it")
    return f.decrypt(mes)


def find_user_element(root, user_name):
    for user in root:
        if user_name == user.find(USER_NAME_SUB_TAG).text:
            return user


def find_file_element(files_root, file_name):
    for file in files_root:
        print(file.text)
        if file.text == file_name:
            return file


def find_client_element(clients_root, address, client_port):
    # func find the client in the root
    # loop goes for every client
    for client in clients_root:
        # the founded client's ip
        ip = client.find(IP_SUB_TAG)
        # the founded client's port
        port = client.find(PORT_SUB_TAG)
        print(client_port)
        # the client parm == the needed client
        if ip.text == address[GO_TO_IP] and port.text == client_port:
            return client


def send_notification(message, ip, port):
    # message - type_of_command  $$  name_of_the_file  $$  ip  $$  port
    # open socket
    client_socket = socket.socket()
    # connect to the client
    client_socket.connect((ip, int(port)))
    # type_of_request  $$  type_of_command  $$  name_of_the_file  $$  ip  $$  port
    # send
    client_socket.send(encrypt((SERVER_REQUEST+SPLITTER_PRO+message).encode()))
    # closing the socket
    client_socket.close()


def send_client_all_files(me_client, clients_root):
    files = []
    # search the client in the root
    for client in clients_root:
        # if the client we found in the loop, is not me_client, then send him his current-files
        if client != me_client:
            # get the client ip
            client_ip = client.find(IP_SUB_TAG).text
            # get the client port
            client_port = client.find(PORT_SUB_TAG).text
            # loop for every file
            for file in client.find(FILES_SUB_TAG):
                # add the tuple in to the list - structure of the tuple: file_name, ip, port
                files.append((file.text, client_ip, client_port))
    for file in files:
        #  type_of_command  $$  name_of_the_file  $$  ip  $$  port
        send_notification(CREATED_COMMAND + SPLITTER_PRO + file[GET_FILE_NAME] +
                          SPLITTER_PRO + file[GET_IP] + SPLITTER_PRO + file[GET_PORT])


def notify_all_clients(me_client, message, root):
    # send notification to all of the clients, except my self
    for client in root:
        if client != me_client:
            # get each client ip, port
            ip = client.find(IP_SUB_TAG).text
            port = client.find(PORT_SUB_TAG).text
            # open threads and sending
            t1 = threading.Thread(target=send_notification, args=(message, ip, port))
            t1.start()


def handle_reg_cmd(path, client, clients_root, client_port, address):
    if not client:  # check if client is exist, if not:
        # set client root in the xml
        client_root = Et.SubElement(clients_root, CLIENT_SUB_TAG)
        # set ip root in the client root
        ip_root = Et.SubElement(client_root, IP_SUB_TAG)
        # put text in ip root
        ip_root.text = address[GO_TO_IP]
        # set port root in the client root
        port_root = Et.SubElement(client_root, PORT_SUB_TAG)
        # put text in port root
        port_root.text = client_port
        # set path root in the client root
        path_root = Et.SubElement(client_root, PATH_SUB_TAG)
        # put text in port root
        path_root.text = path
        # set files root un the client root
        Et.SubElement(client_root, FILES_SUB_TAG)
        send_client_all_files(client_root, clients_root)
    else:
        # print - client - exist
        print("client exist")


def handle_cre_cmd(file_created, client, user):
    print(file_created)
    files_root = client.find(FILES_SUB_TAG)  # open the files root
    file = Et.SubElement(files_root, FILE_SUB_TAG)  # create file root
    root_path = client.find(PATH_SUB_TAG).text  # open the path root
    #  get only the file name, sub the file_created with saved path
    file.text = file_created.split(root_path)[GET_NAME_OF_FILE]  # -1
    clients_root = user.find("clients")
    # send created notification to all the clients
    notify_all_clients(client, CREATED_COMMAND + SPLITTER_PRO + file.text + SPLITTER_PRO+client.find(IP_SUB_TAG).text +
                       SPLITTER_PRO + client.find(PORT_SUB_TAG).text, clients_root)


def handle_del_cmd(deleted_file, client, root):
    # find the client that stored the real file
    root_path = client.find(PATH_SUB_TAG).text  # root_path == where the client save all the files
    file_to_del = deleted_file.split(root_path)[GET_NAME_OF_FILE]  # the file he need to delete
    files_root = client.find(FILES_SUB_TAG)  # get the files root
    for file in files_root:  # search for the file, that the client wants to delete
        if file.text == file_to_del:
            files_root.remove(file)  # delete the file
            # send notification to all of the another clients
            print("delete")
            notify_all_clients(client, DELETED_COMMAND + SPLITTER_PRO +
                               file.text + SPLITTER_PRO + SPACE + SPLITTER_PRO + SPACE, root)


def handle_check_user(client_socket):
    message = "good password and good user name"
    # open threads and sending
    client_socket.send(encrypt(message.encode()))


def handle_modified_command(changed_name, client, root):
    changed_name = changed_name.split(SPLITTER_PATHS)
    new_file_name = ''
    try:
        original_path = changed_name[0]  # 0
        changed_path = changed_name[1]  # 1
    except IndexError:
        # print - the message is not in the right protocol structure, IT WAS NOT SEND BY CLIENT
        print('the message is not in the right protocol structure, IT WAS NOT SEND BY CLIENT')
        return
    root_path = client.find(PATH_SUB_TAG).text  # root_path == where the client save all the files
    file_to_chang_name = original_path.split(root_path)[GET_NAME_OF_FILE]  # the file he need to delete
    files_root = client.find(FILES_SUB_TAG)  # get the files root
    original_path_name = find_file_element(files_root, file_to_chang_name)
    if original_path_name is not None:
        new_file_name = changed_path.split(root_path)[GET_NAME_OF_FILE]
        print("new file name:" + new_file_name)
        original_path_name.text = changed_path.split(root_path)[GET_NAME_OF_FILE]
    notify_all_clients(client, MODIFIED_COMMAND + SPLITTER_PRO + file_to_chang_name + SPLITTER_PATHS + new_file_name
                       + SPLITTER_PRO+client.find(IP_SUB_TAG).text +
                       SPLITTER_PRO + client.find(PORT_SUB_TAG).text, root)


def some_user_have_this_user_name(new_user_name, root):
    for user in root:
        user_name_root = user.find("user_name")
        print(user_name_root.text)
        if user_name_root.text == new_user_name:
            return False
    return True


def handle_change_all_cmd(user_name, password, path, root, client_socket, address, client_port, tree):
    user_name_reg = user_name.split("@@")[0]
    new_user_name = user_name.split("@@")[1]
    user = find_user_element(root, user_name_reg)
    password_reg = password.split("@@")[0]
    new_password = password.split("@@")[1]
    new_path = path.split("@@")[1]

    if user.find("password").text == password_reg and some_user_have_this_user_name(new_user_name, root):
        print("sent good password and user name")
        if new_user_name != "":
            user_name_root = user.find("user_name")
            user_name_root.text = new_user_name
        if new_path != "":
            clients_root = user.find("clients")
            client_root = find_client_element(clients_root, address, client_port)
            path_root = client_root.find("path")
            path_root.text = new_path
        if new_password != "":
            password_root = user.find("password")
            password_root.text = new_password
        message = "updated"
    else:
        message = "this user name is taken"
    client_socket.send(encrypt(message.encode()))
    Et.indent(tree)  # organize the data-base
    # closing the xml + write in Hebrew, use utf-8
    tree.write(XML_SCRIPT_NAME, encoding=USE_HEBREW, xml_declaration=POS_XML_DECLARATION)


def handle_reg_user(user, user_name, password, root, client_socket):
    if not user:  # check if client is exist, if not:
        # set client root in the xml
        user_root = Et.SubElement(root, USER_SUB_TAG)
        # set ip root in the client root
        name = Et.SubElement(user_root, USER_NAME_SUB_TAG)
        # put text in ip root
        name.text = user_name
        # set port root in the client root
        key = Et.SubElement(user_root, PASSWORD_SUB_TAG)
        # put text in port root
        key.text = password
        # set path root in the client root
        Et.SubElement(user_root, CLIENTS_SUB_TAG)
        message = "good"
    else:
        # print - user exist
        print("user exist")
        # sending that user that he is all ready exist
        # get client ip, port
        #  type_of_command  $$  name_of_the_file  $$  ip  $$  port
        message = "this user name is taken"
        # open threads and sending
    client_socket.send(encrypt(message.encode()))


def handle_get_path(client_socket, me_client, clients_root):
    try:
        path = me_client.find("path")
        path = path.text
        client_socket.send(encrypt(path.encode()))
    except AttributeError:
        for client in clients_root:
            if client != me_client:
                path = client.find("path")
                path = path.text
                print(path)
                client_socket.send(encrypt(path.encode()))
                return


def handle_commands(cmd, path, client, clients_root, client_port, address, user,
                    user_name, password, client_socket):
    # for the command in the message, go to his function
    if REGISTER_COMMAND == cmd:  # if the client sent registration command
        handle_reg_cmd(path, client, clients_root, client_port, address)
    if CREATED_COMMAND == cmd:  # if the client created a project
        handle_cre_cmd(path, client, user)
    if DELETED_COMMAND == cmd:  # if the client deleted a project
        handle_del_cmd(path, client, clients_root)
    if CHANGE_NAME == cmd:  # if the client modified a project
        handle_modified_command(path, client, clients_root)
    if CHANGE_PATH_COMMAND == cmd:  # if the client want to change the path
        handle_change_path(path, client)
    if CHECK_USER_COMMAND == cmd:
        handle_check_user(client_socket)
    if GET_MY_PATH_COMMAND == cmd:
        handle_get_path(client_socket, client, clients_root)
    if REGISTER_USER_COMMAND == cmd:
        handle_reg_user(user, user_name, password, root, client_socket)


def check_xml():
    # checking if there is a problem with the xml module
    try:
        f = open("shell", "w")
        f.write(r"<t/>")
        f.close()
        Et.parse("shell")
        os.remove("shell")
    except (NameError, PermissionError):
        # print - You have problem with the xml module, you may need to download again or open the module like this:
        print("You have problem with the xml module, you may need to download again or open the module like this:")
        # print - import xml.etree.ElementTree as ET
        print("import xml.etree.ElementTree as ET")
        return True
    # checking if there is a problem with the xml path
    try:
        # opening the xml data-base
        Et.parse(XML_SCRIPT_NAME)
    except FileNotFoundError:
        # print - cant find the xml path
        print("cant find the xml path")
        return True
    return False


def data_management(user_name, password, cmd, lock, path, client_port, address, client_socket):
    # The lock keeps the xml from failing
    with lock:
        # func that check if there any problem with the opening of the xml file, return false if there is no problem
        if check_xml():
            return
        # opening the xml data-base
        tree = Et.parse(XML_SCRIPT_NAME)
        root = tree.getroot()
        # find the user that stored the real file
        user = find_user_element(root, user_name)
        if cmd == CHANGE_ALL:
            handle_change_all_cmd(user_name, password, path, root, client_socket, address, client_port, tree)
            return
        if cmd != REGISTER_USER_COMMAND:
            # if user == None
            if not user:
                if cmd == CHECK_USER_COMMAND:
                    print("this user name is noe exist in the xml data base:     " + user_name + ", " + password)
                    message = "wrong password or user name"
                    # open threads and sending
                    client_socket.send(encrypt(message.encode()))
                return  # if the user == none and the func isn't check then it was not sent by the goof client protocol 
            if user.find(PASSWORD_SUB_TAG).text == password:
                # find the client that stored the real file
                clients_root = user.find(CLIENTS_SUB_TAG)
                client = find_client_element(clients_root, address, client_port)
                # call the function that handle all types of command
                handle_commands(cmd, path, client, clients_root, client_port, address, user,
                                user_name, password, client_socket)
            else:
                # print - user is exist but wrong password
                print("user is exist, but he sent wrong password:   " + user_name)
                message = "wrong password or user name"
                # open threads and sending
                client_socket.send(encrypt(message.encode()))
        else:
            # find the client that stored the real file
            # call the function that handle all types of command
            handle_reg_user(user, user_name, password, root, client_socket)
        Et.indent(tree)  # organize the data-base
        # closing the xml + write in Hebrew, use utf-8
        tree.write(XML_SCRIPT_NAME, encoding=USE_HEBREW, xml_declaration=POS_XML_DECLARATION)


def handle_client(client_socket, address, lock):
    try:
        message = decrypt(client_socket.recv(BUFFER_SIZE)).decode()
    except (ConnectionRefusedError, ConnectionResetError, socket.error):
        # print - failed to open communication
        print("failed to open communication")
        return
    # message structure - user_name #### password #### cmd  $$  full_path(unless cmd ==reg or user_reg)  $$  client_port
    message = message.split(SPLITTER_DATA)
    print(message)
    try:
        user_name = message[GET_USER_NAME_FROM_MESSAGE]  # 0
        password = message[GET_PASSWORD_FROM_MESSAGE]  # 1
        data = message[GET_DATA_FROM_MESSAGE]  # 2
        message = data.split(SPLITTER_PRO)
        # data structure - cmd  $$  full_path(unless cmd ==reg or user_reg)  $$  client_port
        cmd = message[GO_CMD]  # 0
        path = message[GO_PATH]  # 1
        client_port = message[GO_CLIENT_PORT]  # 2
    except IndexError:
        # print - the message is not in the right protocol structure, IT WAS NOT SEND BY CLIENT!!!
        print('the message is not in the right protocol structure, IT WAS NOT SEND BY CLIENT!!!')
        return
    data_management(user_name, password, cmd, lock, path, client_port, address, client_socket)


if __name__ == '__main__':
    main()
