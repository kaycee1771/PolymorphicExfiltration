import unittest
import requests
from server import app
from encryption import SecureEncryption

class TestClientServerCommunication(unittest.TestCase):
    def setUp(self):
        """Start the Flask test server"""
        self.app = app.test_client()
        self.encryption = SecureEncryption()
        self.test_data = "This is a secret message"
    
    def test_https_data_transfer(self):
        """Test encrypted data transmission via HTTPS"""
        encrypted_data = self.encryption.encrypt(self.test_data)
        response = self.app.post('/upload', data={'payload': encrypted_data})
        
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
