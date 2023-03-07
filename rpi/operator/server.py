import socket
import yaml
from commonFunctions import setupIPs, parseMessage

def receiveMessages(pi_IP):
    TCP_IP = pi_IP 
    TCP_PORT = 5005
    BUFFER_SIZE = 1024 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)
    while 1:
        conn, addr = s.accept()
        print ('Connection address:', addr)
        data = conn.recv(BUFFER_SIZE)
        varSys, varID, varValue = parseMessage(data)
        if not data: break
        print("reveived Sys: ", varSys)
        print("received ID: ", varID)
        print("received data: ", varValue)
        conn.send(data)  # echo
        conn.close()
    return


if __name__  == '__main__':   
    use_case = 'MattHome'
    pi_IP, laptop_IP = setupIPs(use_case)
    receiveMessages(pi_IP)