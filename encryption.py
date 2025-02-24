import os
import socket
import random
import time
import base64
import asyncio
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from sklearn.tree import DecisionTreeClassifier
from dnslib import DNSRecord, QTYPE
import ssl
import numpy as np


# encryption.py (Updated to handle Encryptor and AES encryption for all modes)
class Encryptor:
    def __init__(self, key: bytes):
        self.key = key
        self.iv = os.urandom(16)
        self.backend = default_backend()

    def encrypt(self, data: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        encryptor = cipher.encryptor()
        padded_data = self._pad(data)
        return encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, data: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(data) + decryptor.finalize()
        return self._unpad(decrypted_data)

    def _pad(self, data: bytes) -> bytes:
        padding = 16 - len(data) % 16
        return data + bytes([padding]) * padding

    def _unpad(self, data: bytes) -> bytes:
        return data[:-data[-1]]


# Global Encryptor instance used in all modules
encryptor = Encryptor(os.urandom(32))  # 256-bit key