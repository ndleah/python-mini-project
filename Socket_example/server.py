import socket

HOST = 'localhost' # host where the server is located
PORT = 3000 # port the server is on

s = socket.socket() # new socket with name s
s.bind((HOST, PORT)) # bind host and port to socket
s.listen() # start the server to receive connections

print("Server runing in port ", PORT) # print port address

while True:

    conn, addr = s.accept() # accept connections
    res = conn.recv(1024) # buffer size to receive the data sent from the client

    print('New conection', addr) # print the address of the current connection

    print(res) # print data receive from client

    conn.send(b' Hello from server!') # send data to client

    conn.close() #close the conection
