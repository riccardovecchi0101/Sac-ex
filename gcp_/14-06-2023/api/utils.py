import ipaddress

def check_correctnes_of_parametes(ip:str, netmask:int, gw:str):
    ##checking corectness of ip and gateway:
    print(f"IP IS: {ip} NETMASK IS:{netmask} GATEWAY IS:{gw}")
    try:
        ipaddress.ip_address(ip)
        ipaddress.ip_address(gw)
    except ValueError:
        print("gw or ip not valid\n")
        return False
    
    #checking correctness of network
    ip_net = ip + "/" + str(netmask)
    check_gate = gw + "/" + str(netmask)

    print(f"NETWORK IS {ip_net}")

    try:
        ipaddress.ip_network(ip_net)
    except ValueError:
        print("net not correct\n")
        return False
    
    return True


def check_if_rule_matches(net:str, ip:str):

    print(f"NET IS {net}, IP IS {ip}")
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    
    print("Controllo...")
    return ipaddress.ip_address(ip) in ipaddress.ip_network(net, strict=True)