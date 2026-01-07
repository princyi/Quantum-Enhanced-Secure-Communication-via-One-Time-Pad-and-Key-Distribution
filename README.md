# Btech-Final-year-project
Quantum-Enhanced Secure Communication via One-Time Pad and Key Distribution

📡 Quantum-Enhanced Secure Communication via One-Time Pad & Key Distribution

This repository contains an implementation of a quantum-enhanced secure communication system that combines One-Time Pad (OTP) encryption with quantum key distribution (QKD) to achieve strong theoretical security.

🔐 What This Project Does

Implements unconditionally secure encryption using the One-Time Pad, a classical cryptographic method that is provably secure when the key is truly random and used only once. 
Wikipedia

Uses principles of quantum key distribution to generate and distribute secret keys securely. QKD leverages quantum mechanical properties to detect eavesdropping and ensure both parties share a random key that cannot be intercepted without detection. 
Wikipedia

The generated quantum keys are then applied to encrypt messages with the One-Time Pad, providing perfect secrecy under ideal conditions.

🧠 Why This Matters

Traditional cryptography relies on computational hardness assumptions that could be broken by future quantum computers. By combining QKD with OTP encryption:

Security no longer depends on mathematical assumptions; it becomes information-theoretic. 
Wikipedia

Any attempt at eavesdropping can be detected due to how quantum states behave under measurement. 
Wikipedia

This approach explores next-generation secure communication suitable for high-security environments.

🛠️ Features

Simulation or prototyping of quantum key generation and distribution

Integration of OTP encryption using securely shared keys

Demonstration of message encryption and decryption with information-theoretic security

Research-oriented implementation for academic and practical exploration

📁 Repository Contents

src/ – Source code for the quantum simulator and encryption modules

Quantum_Simulator.py – Python implementation of the QKD-based key distribution and OTP integration

Project reports and research documentation supporting the architecture and algorithms

💡 Technologies Used

Python for simulator and encryption implementation

Algorithms based on quantum cryptography protocols and OTP encryption

📘 Background

The one-time pad achieves perfect secrecy when all conditions are met: the key is random, at least as long as the plaintext, never reused, and shared only between sender and receiver. Quantum key distribution provides a method to share these random keys securely over a quantum channel, enabling practical deployment of OTP-based systems.
