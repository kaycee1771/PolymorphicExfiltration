import os
import random
import platform

class FakeLogs:
    """
    Generates fake log entries to mislead forensic investigations.
    """

    def __init__(self):
        self.fake_log_entries = [
            "User logged in successfully.",
            "System update completed.",
            "Antivirus scan finished. No threats detected.",
            "Security patch applied successfully.",
            "Remote desktop connection established from 192.168.1.10",
        ]

    def write_fake_logs(self):
        """
        Writes fake log entries to system logs (Windows Event Log / Linux syslog).
        """
        log_entry = random.choice(self.fake_log_entries)

        if platform.system() == "Windows":
            os.system(f'eventcreate /ID 1 /L APPLICATION /T INFORMATION /SO "SecurityLog" /D "{log_entry}"')
        elif platform.system() == "Linux":
            os.system(f'logger "{log_entry}"')

        print(f"📜 Fake Log Injected: {log_entry}")

# Example Usage
if __name__ == "__main__":
    logs = FakeLogs()
    logs.write_fake_logs()
