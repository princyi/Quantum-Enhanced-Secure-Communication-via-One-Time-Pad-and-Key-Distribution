import qiskit
from qiskit import QuantumRegister, QuantumCircuit
from qiskit import *
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit_aer import AerSimulator, Aer
import random


def encode(bits, bases):
    """This function encodes each bit into the given basis."""

    encoded_qubits = []
    print(bits, bases)
    for bit, basis in zip(bits, bases):
        qc = QuantumCircuit(1, 1)  # Create a quantum circuit for each qubit

        # Possible Cases
        if bit in ("0", 0) and basis == "Z":
            encoded_qubits.append(qc)  # Do not apply any gates

        elif bit in ("1", 1) and basis == "Z":
            qc.x(0)  # Apply X Gate
            encoded_qubits.append(qc)

        elif bit in ("0", 0) and basis == "X":
            qc.h(0)  # Apply H Gate
            encoded_qubits.append(qc)

        elif bit in ("1", 1) and basis == "X":
            qc.x(0)  # Apply X Gate
            qc.h(0)  # Apply H Gate
            encoded_qubits.append(qc)

    return (encoded_qubits), qc


# qubit = encode([0, 1, 1, 0, 1, 1, 1, 1, 0, 0], 'XXZXXXXXXX')

def generate_random_bases(num_of_bases):
    """This function selects a random basis for each bit"""
    """This function selects a random basis for each bit"""
    bases_string = ""
    for i in range(num_of_bases):
        random_basis = random.randint(0, 1)  # Flip Coin

        if random_basis == 0:
            bases_string += "Z"
        else:
            bases_string += "X"

    return bases_string

def measure(qubits, bases):
    """This function measures each qubit in the corresponding basis chosen for it."""

    bits = ""  # The results of measurements

    for qubit, basis in zip(qubits, bases):

        # Add measurement depending on basis
        if basis == "Z":
            qubit.measure(0, 0)
        elif basis == "X":
            qubit.h(0)
            qubit.measure(0, 0)

        # Execute on Simulator
        simulator = Aer.get_backend('qasm_simulator')
        result = simulator.run(qubit, backend=simulator, shots=1).result()
        counts = result.get_counts()
        measured_bit = max(counts, key=counts.get)  # Max doesn't matter for simulator since there is only one shot.

        bits += measured_bit

    return bits

# measure(qubit, 'XZZXZZZXXX')
