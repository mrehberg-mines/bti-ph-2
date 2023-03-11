import socket
import yaml
import RPi.GPIO as GPIO
from commonFunctions import setupIPs, parseMessage
global bindings

def setupPi(pins:bool ):
    ## create all GPIO bindings for the PI
    # read in yaml data
    with open('gpio_bindings.yaml', 'r') as file:
      bindings = yaml.safe_load(file)

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    if pins:
        for pin in bindings.keys():
            pin_Num = bindings[pin]['pin']
            pin_Type = bindings[pin]['type']
            pin_Defualt = bindings[pin]['initial']

            if pin_Type == 'DO':
                if pin_Defualt == True:
                    GPIO.setup(pin_Num, GPIO.OUT, initial = GPIO.HIGH)
                else:
                    GPIO.setup(pin_Num, GPIO.OUT, initial = GPIO.LOW)
            else: 
                print('Unspecified Pin Type') 
    print('Pin Setup Complete')
    return bindings


def writeCommand(varID, varValue):
    pin_ID = bindings[varID]
    pin_Type = bindings[varID]['type']

    if pin_Type == 'DO':
        if varValue == "True":
            #just putting a pritn statement to not cause an error
            print('high')
            #make out put high
        elif varValue == "False":
            #just putting a pritn statement to not cause an error
            print('low')
            # make output low
        else:
            print('invalid')
            #invalid command entry
            # return an invalid entry
    
    #this is just a placeholder so it will run
    feedback = f'{varID}:{varValue}'
    return str.encode(feedback)


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
        varID, varValue = parseMessage(data)
        feedback = writeCommand(varID, varValue)
        if not data: break
        print("received message: ", data)
        # send back feedback. Should be true unless it was an invalid command
        conn.send(feedback)  
        conn.close()
    return


if __name__  == '__main__':   
    use_case = 'MattHome'
    pi_IP, laptop_IP = setupIPs(use_case)
    bindings = setupPi(pins=False)
    receiveMessages(pi_IP)