import socket
import sys
import select
import errno # errno is module (check if can not to receive msg anymore, get that an error)

BUFFER_SIZE = 10    # constant value
HOST = 'localhost'  # IP of server
PORT = 1367         # port 
c_username = input("Howdy! please tell me what your name... : ")

## create socket
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect((HOST,PORT))
c_socket.setblocking(False) 

## Prepare username
username = c_username.encode('utf-8')
username_header = f"{len(username):<{BUFFER_SIZE}}".encode('utf-8')
c_socket.send(username_header + username)

while True:
    msg = input(f'{c_username} : ')

    if msg:
        msg = msg.encode('utf-8')
        msg_header = f"{len(msg):<{BUFFER_SIZE}}".encode('utf-8')
        c_socket.send(msg_header + msg)

    try:
        while True:
            username_header = c_socket.recv(BUFFER_SIZE)

            if not len(username_header):
                print('Bar closed. ( connection closed by the server )')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = c_socket.recv(username_length).decode('utf-8')

            msg_header = c_socket.recv(BUFFER_SIZE)
            msg_length = int(msg_header.decode('utf-8').strip())
            msg = c_socket.recv(msg_length).decode('utf-8')

            print(f'{username} : {msg}')
            
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
