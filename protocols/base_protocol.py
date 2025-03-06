import time
import random
import socket
import base64

class BaseProtocol:
    """
    Base class for all exfiltration protocols.
    - Supports adaptive timing, encoding, packet size, and noise injection.
    - Uses dynamic mutation to evade detection.
    """

    def __init__(self, name, detection_rate, command, server_ip, delay=0.1, encoding="Base64", packet_size=256, noise=0):
        self.name = name
        self.detection_rate = detection_rate
        self.command = command
        self.server_ip = server_ip
        self.delay = delay  
        self.encoding = encoding
        self.packet_size = packet_size  
        self.noise = noise  # Random noise factor to obfuscate traffic

    def encode_data(self, data):
        """ Encode data based on the selected encoding method. """
        if self.encoding == "Base64":
            return base64.b64encode(data.encode()).decode()
        elif self.encoding == "XOR":
            return ''.join(chr(ord(c) ^ 42) for c in data) 
        elif self.encoding == "AES-Padded":
            return f"AES_ENCRYPTED::{data}"  
        return data 

    def transmit(self, data):
        """ Simulate data transmission and determine if detected. """
        time.sleep(self.delay)  # Apply delay before transmission
        encoded_data = self.encode_data(data)

        # Simulate IDS detection probability
        detected = random.random() < self.detection_rate  
        
        if detected:
            print(f"⚠️ {self.name} Protocol Detected! Adjusting strategy...")

        return not detected  # Transmission success if not detected
