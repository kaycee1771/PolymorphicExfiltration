import unittest
from encryption import SecureEncryption

class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.encryption = SecureEncryption()
        self.test_data = "This is a secret message"

    def test_aes_encryption_decryption(self):
        """Test AES-256-GCM encryption and decryption"""
        encrypted = self.encryption.encrypt(self.test_data)
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(decrypted, self.test_data)

    def test_chacha_encryption_decryption(self):
        """Test ChaCha20-Poly1305 encryption and decryption"""
        encrypted = self.encryption.encrypt(self.test_data, use_chacha=True)
        decrypted = self.encryption.decrypt(encrypted, use_chacha=True)
        self.assertEqual(decrypted, self.test_data)

if __name__ == "__main__":
    unittest.main()
