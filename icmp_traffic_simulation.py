# icmp_traffic_simulation.py

import os
import base64
import socket
import struct
import time
import select
from icmp import ICMP_ECHO_REQUEST, checksum

def send_icmp_command(command: str, server_ip: str):
    """
    Sends a command over ICMP by encoding it into an Echo Request.
    The server will respond with the result of the command.
    """
    # Step 1: Base64 encode the command
    encoded_command = base64.b64encode(command.encode('utf-8')).decode('utf-8')

    # Step 2: Create an ICMP Echo Request packet with the encoded command
    packet = create_icmp_packet(encoded_command)

    # Step 3: Send the ICMP packet to the server
    send_icmp_packet(packet, server_ip)
    print(f"Sent ICMP query with command: {command}")

    # Step 4: Receive the ICMP Echo Reply with the command result
    result = receive_icmp_reply()
    print(f"Received ICMP response with result: {result}")

def create_icmp_packet(encoded_command: str):
    """
    Creates the ICMP packet with the encoded command.
    """
    packet = ICMP_ECHO_REQUEST()
    packet.data = encoded_command
    packet.checksum = checksum(packet)

    return packet

def send_icmp_packet(packet, server_ip):
    """
    Send the ICMP packet to the server.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.sendto(packet.encode(), (server_ip, 0))

def receive_icmp_reply():
    """
    Receive the ICMP Echo Reply and decode the result.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    while True:
        ready = select.select([sock], [], [], 5)
        if ready[0]:
            reply = sock.recv(1024)
            decoded_response = extract_command_result(reply)
            if decoded_response:
                return decoded_response
        else:
            print("No response received.")
            return None

def extract_command_result(reply):
    """
    Extract the decoded result from the ICMP reply packet.
    """
    try:
        icmp_reply = ICMP_ECHO_REPLY(reply)
        command_output = base64.b64decode(icmp_reply.data).decode('utf-8')
        return command_output
    except Exception as e:
        return str(e)
