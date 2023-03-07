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

    return

