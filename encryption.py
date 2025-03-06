import os
import base64
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

class SecureEncryption:
    """
    Implements AES-256-GCM and ChaCha20-Poly1305 encryption with shared key storage.
    """

    KEY_FILE = "shared_key.bin"

    def __init__(self):
        """
        Load or generate a shared encryption key for consistent encryption between client and server.
        """
        if os.path.exists(self.KEY_FILE):
            with open(self.KEY_FILE, "rb") as f:
                self.aes_key = f.read()
        else:
            self.aes_key = AESGCM.generate_key(bit_length=256)
            with open(self.KEY_FILE, "wb") as f:
                f.write(self.aes_key)

        self.chacha_key = self.aes_key  # Use the same key for both AES & ChaCha20

    def encrypt(self, data, use_chacha=False):
        """
        Encrypts data using AES-256-GCM or ChaCha20-Poly1305.
        - Generates a random IV (nonce) for each encryption.
        - Encodes the ciphertext as Base64 for safe transmission.
        """
        data = data.encode()
        iv = os.urandom(12)  # Generate random IV (Nonce)

        cipher = ChaCha20Poly1305(self.chacha_key) if use_chacha else AESGCM(self.aes_key)
        ciphertext = cipher.encrypt(iv, data, None)

        return base64.b64encode(iv + ciphertext).decode()

    def decrypt(self, encrypted_data, use_chacha=False):
        """
        Decrypts data using AES-256-GCM or ChaCha20-Poly1305.
        - Extracts IV from the Base64-encoded encrypted payload.
        """
        try:
            encrypted_data = base64.b64decode(encrypted_data)
            iv, ciphertext = encrypted_data[:12], encrypted_data[12:]

            cipher = ChaCha20Poly1305(self.chacha_key) if use_chacha else AESGCM(self.aes_key)
            return cipher.decrypt(iv, ciphertext, None).decode()
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return None  # Return None to prevent crashes

    def regenerate_key(self):
        """
        Regenerates the shared encryption key (for key rotation purposes).
        """
        self.aes_key = AESGCM.generate_key(bit_length=256)
        with open(self.KEY_FILE, "wb") as f:
            f.write(self.aes_key)

    def secure_wipe_memory(self):
        """
        Clears encryption keys from memory after use.
        """
        self.aes_key = None
        self.chacha_key = None
