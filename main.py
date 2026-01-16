from qkd_simulation import generate_quantum_key, calculate_qber
from otp_encryption import string_to_bits, bits_to_string, xor_encrypt
from automation_controller import security_decision
from genai_security_report import generate_report

# Step 1: Generate quantum key
key = generate_quantum_key(128)

# Step 2: Simulate receiver key
receiver_key = key.copy()
qber = calculate_qber(key, receiver_key)

# Step 3: AI security decision
decision = security_decision(key, qber)

# Step 4: Encrypt if allowed
if decision == "PROCEED":
    message = "HELLO"
    message_bits = string_to_bits(message)
    cipher_bits = xor_encrypt(message_bits, key[:len(message_bits)])
    decrypted = bits_to_string(xor_encrypt(cipher_bits, key[:len(message_bits)]))
    print("Decrypted Message:", decrypted)

# Step 5: Generate AI report
print(generate_report(decision, qber))
