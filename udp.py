import socket
import random


async def send_optimized_udp_packet(data: bytes, server_ip: str, server_port: int):
    packet_size = random.randint(100, 1024)
    if len(data) < packet_size:
        packet = data
    else:
        packet = data[:packet_size]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (server_ip, server_port))
    print(f"Sent {len(packet)} bytes via UDP.")
    await asyncio.sleep(0.1)  # Simulate network delay