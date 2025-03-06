from Crypto.Cipher import AES
import os

class SecureMemoryExfiltrator:
    """
    Stores exfiltrated data in-memory with AES-256 encryption.
    """

    def __init__(self):
        self.key = os.urandom(32)  # Generate a random AES key
        self.nonce = os.urandom(16)  # Generate a unique nonce
        self.memory_buffer = b''  # In-memory storage

    def store_data(self, data):
        """
        Encrypts and stores data in memory.
        """
        self.cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)  # Reinitialize cipher
        encrypted_data, tag = self.cipher.encrypt_and_digest(data.encode())

        self.memory_buffer = encrypted_data  # Store encrypted data
        print(f"🔐 Data stored securely in memory.")

    def read_data(self):
        """
        Reads and decrypts data from memory.
        """
        self.cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)  # Reinitialize cipher
        return self.cipher.decrypt(self.memory_buffer).decode()

    def secure_wipe_memory(self):
        """
        Wipes stored data from memory.
        """
        self.memory_buffer = b''
        print("🧹 Securely erased memory buffer!")
