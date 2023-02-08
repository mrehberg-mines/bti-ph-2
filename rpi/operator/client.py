
import socket
def send_command(varID, varValue):
    TCP_IP = '192.168.0.241' 
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    MESSAGE = f"{varID}:{varValue}"
    byt = MESSAGE.encode()
    while 1:
        byt = MESSAGE.encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(byt)
        data = s.recv(BUFFER_SIZE)
        s.close()
        break

    return data
