import socket, sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = sys.argv[1]
port = int(sys.argv[2])
s.bind((host,port))
s.listen()

conn,addr = s.accept()
data = True
while data:
    data = conn.recv(1024)
    print(data.decode())
