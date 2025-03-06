import random

class GeneticMutator:
    """
    Genetic Algorithm for evolving exfiltration techniques.
    When a protocol is detected frequently, we mutate it.
    """

    def __init__(self):
        self.mutation_options = ["timing", "encoding", "packet_size", "noise", "detection_rate"]

    def mutate_protocol(self, protocol):
        """
        Introduce a mutation to enhance stealth.

        Args:
        - protocol (object): A protocol instance.

        Returns:
        - Mutated protocol (object)
        """
        mutation_type = random.choice(self.mutation_options)

        if mutation_type == "timing":
            protocol.delay = max(0.05, protocol.delay + random.uniform(-0.05, 0.1))
            print(f"🧬 Mutation: Adjusting timing for {protocol.name} → New Delay: {protocol.delay:.2f}s")

        elif mutation_type == "encoding":
            protocol.encoding = random.choice(["Base64", "XOR", "AES-Padded"])
            print(f"🧬 Mutation: Changing encoding for {protocol.name} → New Encoding: {protocol.encoding}")

        elif mutation_type == "packet_size":
            protocol.packet_size = max(100, protocol.packet_size + random.randint(-50, 50))
            print(f"🧬 Mutation: Adjusting packet size for {protocol.name} → New Size: {protocol.packet_size} bytes")

        elif mutation_type == "noise":
            protocol.noise = random.uniform(0, 0.1)
            print(f"🧬 Mutation: Adding random noise to {protocol.name} → Noise Level: {protocol.noise:.2f}")

        elif mutation_type == "detection_rate":
            protocol.detection_rate = max(0.05, protocol.detection_rate - random.uniform(0.01, 0.1))
            print(f"🧬 Mutation: Reducing detection probability for {protocol.name} → New Rate: {protocol.detection_rate:.2f}")

        return protocol 
