from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
RECURSIVE_OPEN = True
CREATED = r"on_created"
DELETED = r"on_deleted"
MODIFIED = r"on_modified"
MOVED = r"on_moved"
SPLITTER_PRO = r'$$'
LINK = r'.lnk'
SPLITTER_DATA = '####'
SPLITTER_PATHS = r'%%'


class MyHandler(FileSystemEventHandler):
    def __init__(self, sender, user_name, password):
        self.sender = sender
        self.User_name = user_name
        self.Password = password

    def on_any_event(self, event):
        print(event.event_type, event.src_path)

    def on_created(self, event):
        print(CREATED, event.src_path)
        # if created occur, send to the server CRATED command
        if not event.src_path.endswith(LINK):
            self.sender.send_message(self.User_name+SPLITTER_DATA
                                     + self.Password+SPLITTER_DATA + CREATED + SPLITTER_PRO + event.src_path)

    def on_deleted(self, event):
        print(DELETED, event.src_path)
        # if deleted occur, send to the server DELETED command
        # if created occur, send to the server CRATED command
        if not event.src_path.endswith(LINK):
            self.sender.send_message(self.User_name+SPLITTER_DATA+self.Password+SPLITTER_DATA+DELETED +
                                 SPLITTER_PRO + event.src_path)

    def on_modified(self, event):
        print(MODIFIED, event.src_path)

    def on_moved(self, event):
        print(MOVED, event.src_path, event.dest_path)
        if not event.src_path.endswith(LINK):
            self.sender.send_message(self.User_name+SPLITTER_DATA+self.Password+SPLITTER_DATA+MOVED
                                 + SPLITTER_PRO + event.src_path + SPLITTER_PATHS + event.dest_path)


class MyObserver:
    def __init__(self, path, user_name, password, message):
        self.PATH = path
        self.event_handler = MyHandler(message, user_name, password)
        self.observer = Observer()

    def run(self):
        print(self.PATH)
        # recursive - search for files in fails
        # observe, check changes in PATH
        try:
            self.observer.schedule(self.event_handler, path=self.PATH, recursive=RECURSIVE_OPEN)
            # starts to observer
            self.observer.start()
        except FileNotFoundError:
            print("the path is bad, please give different path")

    def stop(self):
        # stop observing
        self.observer.stop()
