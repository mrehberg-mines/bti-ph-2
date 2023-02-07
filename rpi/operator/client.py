import socket

TCP_IP = '192.168.0.241' # this IP of my pc. When I want raspberry pi 2`s as a client, I replace it with its IP '169.254.54.195'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Move To Left"
byt = MESSAGE.encode()
while 1:
    MESSAGE = input("Message: ")
    byt = MESSAGE.encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(byt)
    data = s.recv(BUFFER_SIZE)
    s.close()
    print ("received data:", data)