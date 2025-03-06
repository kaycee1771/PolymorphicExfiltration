import random
import numpy as np

class ExfiltrationEnv:
    """
    Simulates network conditions and IDS detection response.
    Different protocols have different chances of detection.
    """

    def __init__(self):
        self.protocols = ["DNS", "HTTPS", "UDP", "ICMP", "WebSocket"]
        self.detection_chance = {
            "DNS": 0.2, 
            "HTTPS": 0.3,
            "UDP": 0.1,
            "ICMP": 0.5,
            "WebSocket": 0.15
        }

    def step(self, action):
        """
        Simulate sending data via a selected protocol.

        Returns:
        - reward (float): +1 if undetected, -1 if detected
        - detected (bool): True if IDS detected the transmission
        """
        protocol = self.protocols[action]
        detected = random.random() < self.detection_chance[protocol]  # Simulate IDS detection
        
        reward = -1 if detected else 1
        return reward, detected  # Return reward and detection status

class RLAgent:
    """
    Reinforcement Learning Agent for Protocol Selection.
    Uses Q-learning to optimize protocol choice.
    """

    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.env = env
        self.q_table = np.zeros((len(env.protocols),))  # Initialize Q-table
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability

    def choose_protocol(self):
        """
        Choose the best protocol (exploitation) or explore randomly.
        """
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, len(self.env.protocols) - 1)
        return np.argmax(self.q_table) 

    def update_q_table(self, action, reward):
        """
        Update Q-table based on reward.
        """
        best_future_q = np.max(self.q_table)
        self.q_table[action] += self.alpha * (reward + self.gamma * best_future_q - self.q_table[action])

    def train(self, episodes=100):
        """
        Train the agent over multiple iterations.
        """
        for _ in range(episodes):
            action = self.choose_protocol()
            reward, detected = self.env.step(action)
            self.update_q_table(action, reward)

            print(f"Episode {_+1}: Protocol {self.env.protocols[action]} - {'DETECTED' if detected else 'SUCCESSFUL'}")

# Running Training
if __name__ == "__main__":
    env = ExfiltrationEnv()
    agent = RLAgent(env)
    agent.train(episodes=50)
