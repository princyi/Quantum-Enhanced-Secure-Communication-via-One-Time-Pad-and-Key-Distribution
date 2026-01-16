import random

def generate_quantum_key(length=128):
    # Simulated quantum randomness
    key = [random.choice([0, 1]) for _ in range(length)]
    return key

def calculate_qber(sender_key, receiver_key):
    mismatches = sum(1 for a, b in zip(sender_key, receiver_key) if a != b)
    return mismatches / len(sender_key)
