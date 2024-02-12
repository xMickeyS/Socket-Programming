import socket 
import select # select is module gives us OS-level monitoring operation for thing ( monitor many connect simutaneoly )

BUFFER_SIZE = 10    # constant value
HOST = 'localhost'  # IP of server
PORT = 1367        # port (367 is my lucky number hehe~)

## create and setup the socket
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = ipv4 and SOCK_STREAM = TCP  # AF stand for Address Family !
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow to reuse the address 

## bind a socket to some port
s_socket.bind((HOST, PORT))

## wait for client to connect
s_socket.listen()

sockets_list = [s_socket] # create a list of sockets for select module to keep track
clients = {} # dict of conneted clients

print(f'Bartender is waiting on {HOST}:{PORT}...')

def receive_message(client_socket):
    try:
        msg_header = client_socket.recv(BUFFER_SIZE) # socket is going to attempt to receive data, in a buffer size 1024 byte

        # if received no data, closed a connection
        if not len(msg_header):
            return False
    
        msg_length = int(msg_header.decode("utf-8").strip()) # convert header to int value

        return {"header" : msg_header, "data": client_socket.recv(msg_length)} # return object (header, clients data)

    except:
        return False
    
while True:
    # select has 3 parameters rlist (sockets to be monitored for incoming) wlist (socket for data to send to) and x list (socket to be monitored for exception)
    # return reading, writing ,and errors
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # iterate notified socket (for i in read_sockets)
    for notified_socket in read_sockets:

        # new socket
        if notified_socket == s_socket:
            # new connection, accept
            # accepts will give us new socket (clinet_socket) and returned ip/port set
            client_socket, client_address = s_socket.accept() 

            # client should send name right away
            user = receive_message(client_socket)

            # if client not send name, disconnected 
            if user is False:
                continue

            # append accepted socket to list
            sockets_list.append(client_socket)

            # save username and username header
            clients[client_socket] = user

            
            print(f"{user['data'].decode('utf-8')} from {client_address[0]}:{client_address[1]} join the table.")
        
        # existing socket
        else:
            
            msg = receive_message(notified_socket)
            
            # if client disconnected, cleaup
            if msg is False:
                print(f"{clients[notified_socket]['data'].decode('utf-8')} left.")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            # get user by notified socket
            user = clients[notified_socket]
            username = user['data'].decode('utf8')

            print(f"{username} said {msg['data'].decode('utf-8')}")

            #  Iterate over connected clients and broadcast message
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + msg['header'] + msg['data'])
                                       
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]