from collections import defaultdict
import random
import math

class MarkovPredictor:
    """
    Advanced Markov Chain for Predictive Protocol Switching.
    - Uses weighted success rates (newer successes matter more).
    - Implements a decay factor for older transitions.
    - Uses confidence threshold before switching.
    """

    def __init__(self, decay_factor=0.9, confidence_threshold=0.6):
        """
        decay_factor (float): How fast older transitions lose importance (0.0 to 1.0).
        confidence_threshold (float): Minimum confidence required before switching.
        """
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        self.success_counts = defaultdict(lambda: defaultdict(int))
        self.last_used = defaultdict(int)  # Tracks when a protocol was last used
        self.decay_factor = decay_factor
        self.confidence_threshold = confidence_threshold

    def update(self, prev_protocol, new_protocol, success):
        """
        Update the Markov Chain with the latest protocol switch.
        Applies decay factor to older data.
        """
        # Apply decay to previous transitions
        for protocol in self.transition_counts[prev_protocol]:
            self.transition_counts[prev_protocol][protocol] *= self.decay_factor
            self.success_counts[prev_protocol][protocol] *= self.decay_factor
        
        # Increment counters for new transition
        self.transition_counts[prev_protocol][new_protocol] += 1
        if success:
            self.success_counts[prev_protocol][new_protocol] += 1

        # Update last used timestamp
        self.last_used[new_protocol] += 1

    def predict_next(self, current_protocol):
        """
        Predicts the best protocol to use next.
        - Uses weighted success rate.
        - Only switches if confidence is above the threshold.
        """

        if current_protocol not in self.transition_counts:
            return random.choice(list(self.transition_counts.keys()))  # Pick randomly if no history
        
        transitions = self.transition_counts[current_protocol]
        successes = self.success_counts[current_protocol]

        # Compute weighted success rates
        success_rates = {}
        for protocol in transitions:
            if transitions[protocol] > 0:
                weight = math.exp(-0.1 * self.last_used[protocol])  # Recent protocols are weighted higher
                success_rates[protocol] = weight * (successes[protocol] / transitions[protocol])

        # Choose the protocol with the highest weighted success rate
        if success_rates:
            best_protocol, confidence = max(success_rates.items(), key=lambda x: x[1])

            # Only switch if confidence is above the threshold
            if confidence >= self.confidence_threshold:
                print(f"🔄 Markov Prediction: Switching to {best_protocol} (Confidence: {confidence:.2f})")
                return best_protocol

        # If confidence is low, stay with the current protocol
        print(f"🤔 Markov Decision: Staying with {current_protocol} (Low confidence)")
        return current_protocol
