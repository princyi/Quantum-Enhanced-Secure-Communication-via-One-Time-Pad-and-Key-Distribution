import hashlib, hmac, binascii
import requests
import random
import hashlib
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

API_KEY = 'AdKSKlIQmF1cQHVFOg0rC5PktWNlVGz35Vlg0IOD'
API_URL = "https://api.quantumnumbers.anu.edu.au"

DTYPE = "uint16"  # uint8, uint16, hex8, hex16
BLOCKSIZE = 1  # between 1--10. Only needed for hex8 and hex16


def scrypt_key_derivation(password, salt, length):
    key = scrypt(password.encode(), salt, length, N=2 ** 14, r=length, p=1)
    return b64encode(key).decode()


def generate_quantum_random_key(length):
    params = {"length": 1024, "type": DTYPE,}
    headers = {"x-api-key": API_KEY}
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        js = response.json()
        if js["success"] == True:
            key = ''.join([str(elem) for elem in js["data"]])
            key = pad(key.encode(), length)
            key = b64encode(key).decode()
            key2 = list(map(''.join, zip(*[iter(key)] * length)))
            key2 = random.choice(key2)
            return key2
        else:
            return js["message"]

    else:
        return response.text


def xor_bytes(data, key):
    """XOR two byte strings."""
    print(key)
    print(data)
    return bytes([b ^ k for b, k in zip(data, key)])


def encrypt(message, key):
    """Encrypt a message using the one-time pad."""

    # if len(message) != len(key):
    #     raise ValueError("Key length must be equal to message length.")
    encrypted_message = xor_bytes(str.encode(message), str.encode(key))
    key = b64encode(str.encode(key)).decode('utf-8')
    encrypted_message = b64encode(encrypted_message).decode('utf-8')
    return encrypted_message, key


def decrypt(message, key):
    """Decrypt a message using the one-time pad."""
    if len(message) != len(key):
        raise ValueError("Key length must be equal to ciphertext length.")
    decrypted_message = xor_bytes(b64decode(message), b64decode(key))
    return decrypted_message.decode()


def generate_hash(key, message):
    key_and_message = key+message
    hashed_key_and_message = hashlib.sha512(key_and_message.encode('utf-8')).hexdigest()
    return hashed_key_and_message
