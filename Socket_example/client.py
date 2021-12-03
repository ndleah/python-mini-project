import socket

HOST = 'localhost' # host where the server is located
PORT = 3000 # port the server is on

s = socket.socket() # new socket with name s

s.connect((HOST, PORT)) # connection to server

s.send(b"Hello from client") # send message to server
res = s.recv(1024) # buffer size to receive the data sent from the server

print(res) # print the data
s.close() # close the connection with server
