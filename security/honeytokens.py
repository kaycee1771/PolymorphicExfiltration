import os
import random
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class HoneytokenMonitor(FileSystemEventHandler):
    """
    Monitors honeytokens for unauthorized access, modification, or deletion.
    """

    def __init__(self, honeytoken_manager):
        super().__init__()
        self.honeytoken_manager = honeytoken_manager

    def on_modified(self, event):
        if event.src_path in self.honeytoken_manager.file_paths:
            print(f"🚨 ALERT: {event.src_path} was modified!")
            self.honeytoken_manager.trigger_countermeasures(event.src_path)

    def on_deleted(self, event):
        if event.src_path in self.honeytoken_manager.file_paths:
            print(f"🚨 ALERT: {event.src_path} was deleted!")
            self.honeytoken_manager.trigger_countermeasures(event.src_path)

    def on_moved(self, event):
        if event.src_path in self.honeytoken_manager.file_paths:
            print(f"🚨 ALERT: {event.src_path} was moved to {event.dest_path}!")
            self.honeytoken_manager.trigger_countermeasures(event.src_path)

class Honeytokens:
    """
    Deploys fake sensitive files (honeytokens) and detects unauthorized access.
    """

    def __init__(self, monitor_directory="honeytokens/"):
        self.monitor_directory = monitor_directory
        self.files = {
            "passwords.txt": "admin:123456\nroot:password\nuser:qwerty",
            "api_keys.json": '{"google_api_key": "AIzaSyEXAMPLE", "aws_access_key": "AKIAXXXXXX"}',
            "bank_statement.pdf": "Fake bank statement data..."
        }
        self.file_paths = []
        self.observer = Observer()

        if not os.path.exists(self.monitor_directory):
            os.makedirs(self.monitor_directory)
            print(f"📁 Created honeytoken directory: {self.monitor_directory}")

    def deploy_honeytokens(self):
        """Creates fake sensitive files and starts real-time monitoring."""
        for filename, content in self.files.items():
            file_path = os.path.join(self.monitor_directory, filename)
            with open(file_path, "w") as f:
                f.write(content)
            self.file_paths.append(file_path)

        # Start real-time monitoring
        event_handler = HoneytokenMonitor(self)
        self.observer.schedule(event_handler, self.monitor_directory, recursive=True)
        self.observer.start()
        print("🛑 Honeytokens deployed and actively monitored!")

    def trigger_countermeasures(self, file_path):
        """Adaptive response when a honeytoken is accessed."""
        print(f"🚨 Unauthorized access to {file_path}! Executing countermeasures...")

        response = random.choice(["shutdown", "log_forgery", "protocol_switch", "self_delete"])

        if response == "shutdown":
            print("🛑 SYSTEM SHUTDOWN INITIATED!")
            os.system("shutdown /s /t 10")  # Windows shutdown (Linux: `os.system("shutdown -h now")`)

        elif response == "log_forgery":
            print("📜 Forging logs to mislead forensic analysts...")
            os.system(f'eventcreate /ID 1 /L APPLICATION /T INFORMATION /SO "SecurityLog" /D "Unauthorized access to critical file detected. Investigation required."')

        elif response == "protocol_switch":
            print("🔄 Switching to backup protocol...")
            os.system("python protocol_switcher.py --use_backup")

        elif response == "self_delete":
            print("🧨 Self-destructing all honeytokens and related logs!")
            self.delete_honeytokens()
            os.remove(__file__)

    def delete_honeytokens(self):
        """Deletes all honeytokens and stops monitoring."""
        for file_path in self.file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
        self.observer.stop()
        print("🧹 Honeytokens deleted.")
