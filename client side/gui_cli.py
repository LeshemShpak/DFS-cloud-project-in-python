import PySimpleGUI as Sg
import threading
DFS_GUI = r'dfs_gui'
DO_YOU_HAVE_AN_ACCOUNT = 'Do you have an account?'
YES = 'yes'
NO = 'no'
HALLO = 'Hallo'
YOUR_DATA = 'your data'
ENTER_USER_NAME = 'Enter user name'
ENTER_PASSWORD = 'Enter password'
USER_NAME_TAG = "user_name"
PASSWORD_TAG = "password"
PATH_TAG = "path"
SEND = 'send'
IDENTIFICATION = 'identification'
TRY_AGAIN = "wrong password or user name please try again"
CHANGE_ACCOUNT_SETTINGS = 'you are in the system, do you wants to change your account settings?'
ENTER_NEW_USER_NAME = 'Enter new user name'
ENTER_NEW_PASSWORD = 'Enter new password'
ENTER_NEW_PATH = 'Enter new path'
ACCOUNT_SETTINGS = 'account settings'
PLEASE_CHOOSE = 'please choose user name, password and path'
REGISTER = 'Register'
PLEASE_GIVE_DIFFERENT_USER_NAME = "please give different user name"
YOU_HAVE_BEEN_REGISTERED = "you have been registered"
SPACE = ' '
LIST = []
DOWNLOAD_TKINTER = "you need to download tkinter"
CHANGE_ALL = "change_all_cmd"
REGISTER_USER_COMMAND = r'user_register'
CHECK_USER_COMMAND = r'check_user'
REGISTER_COMMAND = r'register'
GET_MY_PATH_COMMAND = r'get_path'
password = ""
user_name = ""
path = ""


class GUI:
    def __init__(self, sender):
        self.sender = sender

    def run(self,):
        self.check_all_module_gui()
        Sg.theme("DarkGrey7")
        # All the stuff inside your window.
        layout = [[Sg.Text(DO_YOU_HAVE_AN_ACCOUNT)], [Sg.Button(YES), Sg.Button(NO)]]
        have_a = False
        # Create the Window
        window = Sg.Window(HALLO, layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == Sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break
            if event == YES:  # if user have an account
                have_a = True
                break
            if event == NO:  # if user don't have an account
                break
        # close the first Window
        window.close()
        # second window
        if have_a:  # if the user have an account
            self.handle_account()
        else:  # if user don't have an account
            self.create_account()

    def check_all_module_gui(self):
        try:
            Sg.Window(SPACE, LIST)
        except ModuleNotFoundError:
            print(DOWNLOAD_TKINTER)

    def get_path(self):
        return path

    def get_password(self):
        return password

    def get_user_name(self):
        return user_name

    def get_path(self):
        path = self.sender.send_and_rec(
            user_name + "####" + password + "####" + GET_MY_PATH_COMMAND + "$$")
        print(path)
        return path

    def open_third(self):
        # All the stuff inside your window. - you are in the system, do you wants to change your account settings?
        layout = [[Sg.Text(CHANGE_ACCOUNT_SETTINGS)],
                  [Sg.Text(ENTER_NEW_USER_NAME), Sg.InputText(key=USER_NAME_TAG)],
                  [Sg.Text(ENTER_NEW_PASSWORD), Sg.InputText(key=PASSWORD_TAG)],
                  [Sg.Text(ENTER_NEW_PATH), Sg.InputText(key=PATH_TAG)],
                  [Sg.Button(SEND)]
                  ]
        #  opening the third screen
        window = Sg.Window(ACCOUNT_SETTINGS, layout)
        global path
        while True:
            event, values = window.read()
            if event == Sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break
            if event == SEND:  # sending the server the new account settings
                new_user_name = values[USER_NAME_TAG]
                new_password = values[PASSWORD_TAG]
                new_path = values[PATH_TAG]
                # the func send all the changes
                mes = self.sender.send_and_rec(
                    user_name + "@@" + new_user_name + "####" + password + "@@" + new_password + "####" +
                    CHANGE_ALL + "$$" + path + "@@" + new_path)
                if mes == "updated":
                    print(mes)
                    Sg.popup("updated the server")
                elif mes == "this user name is taken":
                    print(mes)
                    Sg.popup("this user name is taken")
                else:
                    print("problem")
                    Sg.popup("problem with the server")
        # closing the third screen
        window.close()
        print(path)

    def handle_account(self):
        open_next = False
        # All the stuff inside your window.
        layout = [[Sg.Text(YOUR_DATA)],
                  [Sg.Text(ENTER_USER_NAME), Sg.InputText(key=USER_NAME_TAG)],
                  [Sg.Text(ENTER_PASSWORD), Sg.InputText(key=PASSWORD_TAG)],
                  [Sg.Button(SEND)]
                  ]
        # Create the Window
        window = Sg.Window(IDENTIFICATION, layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == Sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break
            if event == SEND:
                global user_name, password, path
                user_name = values[USER_NAME_TAG]
                password = values[PASSWORD_TAG]
                #  Confirmation from the server that the client is exists, and he sent the right password and user name
                mes = self.sender.send_and_rec(
                    user_name + "####" + password + "####" + CHECK_USER_COMMAND + "$$" + path)
                if mes == "good password and good user name":
                    print(mes)
                    exists = True
                    self.sender.send_message(
                        user_name + "####" + password +"####" + REGISTER_COMMAND + "$$" + path)
                elif mes == "wrong password or user name":
                    print(mes)
                    exists = False
                else:
                    print("problem")
                if exists:
                    open_next = True
                    break
                else:
                    #  opening a screen with this message - wrong password or user name please try again
                    Sg.popup(TRY_AGAIN)
        # close the sec Window
        window.close()
        # get the path first, the client mast know what path to observer
        path = self.get_path()
        #  if the client is exists, and sent the right data
        #  now s/he can change the path, password and user name.
        if open_next:
            t1 = threading.Thread(target=self.open_third())
            t1.start()


    def create_account(self):
        # All the stuff inside your window. - please choose user name, password and path
        layout = [[Sg.Text(PLEASE_CHOOSE)],
                  [Sg.Text(ENTER_NEW_USER_NAME), Sg.InputText(key=USER_NAME_TAG)],
                  [Sg.Text(ENTER_NEW_PASSWORD), Sg.InputText(key=PASSWORD_TAG)],
                  [Sg.Text(ENTER_NEW_PATH), Sg.InputText(key=PATH_TAG)],
                  [Sg.Button(SEND)],
                  ]
        # opening the registration screen, sec screen
        window = Sg.Window(REGISTER, layout)
        while True:
            event, values = window.read()
            if event == Sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break
            if event == SEND:  # sending the new account settings
                global user_name, password, path
                user_name = values[USER_NAME_TAG]
                password = values[PASSWORD_TAG]
                path = values[PATH_TAG]
                # send, return bool, if true - this user name is taken and the client need to choose different user name
                # ,if false - the server have completed the registration process
                # user_name_is_taken = send_new_account(user_name, password, path)
                mes = self.sender.send_and_rec(user_name + "####" + password +"####" + REGISTER_USER_COMMAND + "$$" + path)
                if mes == "good":
                    user_name_is_taken =False
                    self.sender.send_message(
                        user_name + "####" + password +"####" + REGISTER_COMMAND + "$$" + path)
                elif mes == "this user name is taken":
                    user_name_is_taken = True
                else:
                    #Fkjrjdfrfjmk
                    print("problem")
                if user_name_is_taken:
                    Sg.popup(PLEASE_GIVE_DIFFERENT_USER_NAME)
                else:
                    Sg.popup(YOU_HAVE_BEEN_REGISTERED)
                    break
        # closing the sec window
        window.close()



