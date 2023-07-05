# DFS-cloud-project-in-python

This project is a distributed file system (DFS) implemented in Python. It allows users to store and manage files on a server and access them from multiple clients. The project consists of server-side and client-side code.

## Server-side code

The server-side code handles the communication and file management on the server. Here is an overview of the main components and functionalities:

- **Socket communication**: The server uses socket programming to establish communication with clients.
- **XML data storage**: User and client information is stored in an XML data file (`users.xml`).
- **File encryption**: The server uses the `cryptography` library to encrypt and decrypt messages and file data.
- **Server request handling**: The server receives requests from clients and processes them based on the command type.
- **Client registration**: When a client connects to the server, it registers the client by storing its IP, port, and path in the XML data file.
- **File creation, deletion, and modification**: The server handles commands from clients to create, delete, and modify files.
- **Notification to other clients**: When a file is created, deleted, or modified by a client, the server notifies other connected clients about the changes.
- **User management**: The server handles user registration, checks user credentials, and allows users to update their information.

## Client-side code

The client-side code allows users to interact with the server and manage their files. Here is an overview of the main components and functionalities:

- **Socket communication**: The client uses socket programming to establish communication with the server.
- **File observation**: The client utilizes the `watchdog` library to monitor changes in a specified directory.
- **GUI interface**: The client provides a graphical user interface (GUI) for users to interact with the system.
- **File synchronization**: When changes are detected in the observed directory, the client sends requests to the server to synchronize the changes.
- **File transfer**: The client can request files from the server and receive them for local access.
- **Icon creation**: The client creates shortcut icons for files stored on the server to provide quick access.

## Usage

To use this DFS project, follow these steps:

1. Clone the project repository from GitHub.
2. Install the required libraries (`cryptography`, `watchdog`, `win32com`, and `gui_cli`).
3. Start the server-side code by running the `server.py` file.
4. Start the client-side code by running the `client.py` file.
5. In the client GUI, enter the server IP, port, username, password, and the local directory to observe.
6. Connect to the server and start managing your files through the GUI.

Note: Make sure to modify the `SERVER_IP` and `SERVER_PORT` variables in the client-side code to match your server's IP address and port.

Enjoy using the DFS Cloud Project in Python!
