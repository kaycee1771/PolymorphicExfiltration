# icmp.py

import struct
import socket


# ICMP Types (Echo Request and Echo Reply)
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0


def checksum(source_string):
    """
    A function to calculate the checksum of the given source string.
    Used to ensure the integrity of the ICMP packet.
    """
    # Calculate the checksum for a given source string.
    if len(source_string) % 2:
        source_string += b'\0'
    
    result = 0
    for i in range(0, len(source_string), 2):
        result += (source_string[i] << 8) + (source_string[i + 1])
        result = result & 0xFFFFFFFF  # Keep the result within 32 bits
    result = (result >> 16) + (result & 0xFFFF)
    result += (result >> 16)
    return ~result & 0xFFFF


class ICMP_ECHO_REQUEST:
    """
    This class represents an ICMP Echo Request packet.
    """
    def __init__(self, data):
        self.type = ICMP_ECHO_REQUEST
        self.code = 0
        self.checksum = 0
        self.id = 1  # Arbitrary ID for the Echo Request
        self.sequence = 1
        self.data = data

    def encode(self):
        """
        Encodes the ICMP Echo Request into a packet.
        """
        header = struct.pack('!BBHHH', self.type, self.code, self.checksum, self.id, self.sequence)
        packet = header + self.data.encode('utf-8')
        self.checksum = checksum(packet)
        header = struct.pack('!BBHHH', self.type, self.code, self.checksum, self.id, self.sequence)
        return header + self.data.encode('utf-8')


class ICMP_ECHO_REPLY:
    """
    This class represents an ICMP Echo Reply packet.
    """
    def __init__(self, icmp_request):
        self.type = ICMP_ECHO_REPLY
        self.code = 0
        self.checksum = 0
        self.id = icmp_request.id
        self.sequence = icmp_request.sequence
        self.data = icmp_request.data

    def encode(self):
        """
        Encodes the ICMP Echo Reply into a packet.
        """
        header = struct.pack('!BBHHH', self.type, self.code, self.checksum, self.id, self.sequence)
        packet = header + self.data.encode('utf-8')
        self.checksum = checksum(packet)
        header = struct.pack('!BBHHH', self.type, self.code, self.checksum, self.id, self.sequence)
        return header + self.data.encode('utf-8')


# Additional functions like checksum can be used as shown for integrity
