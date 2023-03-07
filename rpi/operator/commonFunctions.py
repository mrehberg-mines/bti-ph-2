import yaml

def setupIPs(use_case):
    with open('ips.yaml', 'r') as file:
      ips = yaml.safe_load(file)
    
    if use_case == 'Mines':
        pi_IP = ips['mines_pi_wifi']
        laptop_IP = ips['mines_desktop_wifi']
    
    if use_case == 'MattHome':
        pi_IP = ips['matt_pi_wifi']
        laptop_IP = ips['matt_desktop_wifi']
    print(pi_IP)
    return pi_IP, laptop_IP

def parseMessage(message):
    strMessage = message.decode("utf-8")
    varSys = strMessage.split(':')[0]
    varID = strMessage.split(':')[1]
    varValue = strMessage.split(':')[2]
    return varSys, varID, varValue

