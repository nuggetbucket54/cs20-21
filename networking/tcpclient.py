import socket,sys

host = sys.argv[1]
port = int(sys.argv[2])
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((host,port))
data = input('Send data: ')
s.sendall(data.encode())
s.close()
