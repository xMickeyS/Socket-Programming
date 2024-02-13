import os
import socket

# CONSTANT 
IP = 'localhost'  # IP of server
PORT = 1367         # port 
CLIENT_FOLDER = 'client_folder'

## create socket
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect((IP,PORT))

print("> Client connected.")
while(True):
    dir_name = input(">>> Enter filename wanting to tranfer (empty input will send all of file in client_folder)\n> ")
    if(dir_name != ''):
        if os.path.exists(os.path.join(CLIENT_FOLDER, dir_name)):
            path = os.path.join(CLIENT_FOLDER, dir_name)
            folder_name = path.split("/")[-1]
            break
        else:
            print('> The File does not exist.')
            continue

    else: 
        path = os.path.join(CLIENT_FOLDER)
        folder_name = path
        break
    

# send the file name to server
print(f'> Client sending folder named {folder_name}')
c_socket.send(folder_name.encode('utf-8'))
# receive reply form the server
msg = c_socket.recv(1024).decode('utf-8')
print(f"> {msg} ")
print("------------------------------------------")

# send the data
files = sorted(os.listdir(path)) # listdir returns the list of all files and directories in the specified path. 

# loop in list of all files
for file_name in files: 
    # send the file name 
    if os.path.isdir(os.path.join(path, file_name)):
        continue

    msg = f"FILENAME:{file_name}"
    print(f"> Client is sending file name : {file_name}")
    c_socket.send(msg.encode('utf-8'))

    # receive the reply formm the server
    msg = c_socket.recv(1024).decode('utf-8')
    print(f"> {msg}")

    # sent the data
    file = open(os.path.join(path, file_name), "r")
    file_data = file.read()

    msg = f"DATA:{file_data}"
    c_socket.send(msg.encode('utf-8'))
    msg = c_socket.recv(1024).decode('utf-8')
    print(f"> {msg}")

    # close
    msg = f"FINISH:Complete data send"
    c_socket.send(msg.encode('utf-8'))
    msg = c_socket.recv(1024).decode('utf-8')
    print(f"> {msg}\n")

# closing the connection
msg = f"CLOSE:file transfer is completed"
c_socket.send(msg.encode('utf-8'))
c_socket.close()
