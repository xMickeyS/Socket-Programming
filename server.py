import os
import socket 

# CONSTANT VALUES
IP = 'localhost'  # IP of server
PORT = 1367        # port (367 is my lucky number hehe~)
SERVER_FOLDER = 'server_folder'

## create socket
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = ipv4 and SOCK_STREAM = TCP  # AF stand for Address Family !

## bind a socket to some port
s_socket.bind((IP, PORT))

## wait for client to connect
s_socket.listen()
print('> Server is waiting for client.')

while True:
    conn, address = s_socket.accept() # accept() return coon, new socket object usable to send and receive data, and address (ip, port)
    print(f">> Client from {address[0]}:{address[1]} connected.")
    conn.send(f"200 Client connected.".encode('utf-8'))

    # receive the folder name from cilent
    folder_name = conn.recv(1024).decode('utf-8')

    # creating the folder
    path = os.path.join(SERVER_FOLDER, folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
        conn.send(f"20 Folder {folder_name} craeted.".encode("utf-8"))
    else:
        conn.send(f"25 Folder {folder_name} already exits".encode("utf-8"))

    # receiving file
    while True:
        msg = conn.recv(1024).decode('utf-8')

        cmd, data = msg.split(":")

        if cmd == "FILENAME":
            print(f"> Client sent the filename: {data}.")
            file_path = os.path.join(path, data)
            file = open(file_path, "w")
            conn.send("300 Filename received.".encode('utf-8'))

        elif cmd == "DATA":
            print(f"> Client receiving the file data.")
            file.write(data)
            conn.send("301 File data received".encode('utf-8'))

        elif cmd == "FINISH":
            file.close()
            print(f"> Client {data}.\n")
            conn.send(f"302 {data} is saved on server.".encode('utf-8'))

        elif cmd == "CLOSE":
            conn.close()
            print(f"{data}")
            print("------------------------------------------")
            break
