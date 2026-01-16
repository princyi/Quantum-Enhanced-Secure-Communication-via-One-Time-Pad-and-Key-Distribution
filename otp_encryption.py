def xor_encrypt(message_bits, key_bits):
    return [m ^ k for m, k in zip(message_bits, key_bits)]

def string_to_bits(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def bits_to_string(bits):
    chars = []
    for i in range(0, len(bits), 8):
        chars.append(chr(int(''.join(map(str, bits[i:i+8])), 2)))
    return ''.join(chars)
