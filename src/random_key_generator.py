# Use Braket SDK Cost Tracking to estimate the cost to run this example
from braket.tracking import Tracker
t = Tracker().start()

# AWS imports: Import Braket SDK modules
from braket.circuits import Circuit
from braket.devices import Devices, LocalSimulator
from braket.aws import AwsDevice, AwsQuantumTask

# general math imports
import math
import numpy as np
from scipy.fft import fft, ifft

# magic word for producing visualizations in notebook
# %matplotlib inline

# import convex solver
import cvxpy as cp

rigetti, ionq, simulator, device = None, None, None, None


def setup_devices(device_type):
    global device
    device = LocalSimulator()

    if device_type == 'quantum_gate':
        # set up Rigetti quantum device
        global rigetti
        global ionq
        rigetti = AwsDevice(Devices.Rigetti.AspenM3)
        ionq = AwsDevice(Devices.IQM.Garnet)
        return device, rigetti, ionq

    elif device_type == 'classical_gate':
        # simulator alternative: set up the on-demand simulator SV1
        global simulator
        simulator = AwsDevice(Devices.Amazon.SV1)
        return device, simulator



# function for Hadamard cirquit
def hadamard_circuit(n_qubits):
    """
    function to apply Hadamard gate on each qubit
    input: number of qubits
    """

    # instantiate circuit object
    circuit = Circuit()

    # apply series of Hadamard gates
    for i in range(n_qubits):
        circuit.h(i)

    return circuit


def create_quantum_circuit(n):
    # quantum circuit for generating weakly random bit string one
    n1_qubits = 1
    m1_shots = n
    state1 = hadamard_circuit(n1_qubits)
    result1 = device.run(state1, shots=m1_shots).result()
    array_one = result1.measurements.reshape(1, m1_shots * n1_qubits)
    # print(array_one)

    # quantum circuit for generating weakly random bit string two
    n2_qubits = 1
    m2_shots = n
    state2 = hadamard_circuit(n2_qubits)
    result2 = device.run(state2, shots=m2_shots).result()
    array_two = result2.measurements.reshape(1, m2_shots * n2_qubits)
    # print(array_two)

    return array_one, array_two


def toeplitz_constructor(array_one, array_two, m, n):
    # setting up arrays for FFT implementation of Toeplitz
    array_two_under = np.array(array_two[0, 0:n - m])[np.newaxis]
    zero_vector = np.zeros((1, n + m - 3), dtype=int)
    array_two_zeros = np.hstack((array_two_under, zero_vector))
    array_two_over = array_two[0, n - m:n][np.newaxis]
    array_one_merged = np.zeros((1, 2 * n - 3), dtype=int)
    for i in range(m):
        array_one_merged[0, i] = array_one[0, m - 1 - i]
    for j in range(n - m - 1):
        array_one_merged[0, n + m - 2 + j] = array_one[0, n - 2 - j]

    # FFT multplication output of Toeplitz
    output_fft = np.around(ifft(fft(array_one_merged) * fft(array_two_zeros)).real)
    output_addition = output_fft[0, 0:m] + array_two_over
    output_final = output_addition.astype(int) % 2
    # print(f"The {m} random output bits are:\n{output_final}.")
    return output_final


def create_quantum_task(device_type, array_one, array_two, n):
    if device_type == 'quantum_gate':
        #alternative via on-demand simulator SV1

        #quantum circuit for generating weakly random bit string one (simulate Rigetti source)
        n1_q = 1  # alternatively run multiple qubits in parallel
        m1_s = int(math.ceil(n/n1_q))
        state1 = hadamard_circuit(n1_q)
        result1 = simulator.run(state1, shots=m1_s).result()
        array_rigetti = result1.measurements.reshape(1,m1_s*n1_q)

        # quantum circuit for generating weakly random bit string two (simulate IonQ source)
        n2_q = 1  # alternatively run multiple qubits in parallel
        m2_s = int(math.ceil(n/n2_q))
        state2 = hadamard_circuit(n2_q)
        result2 = simulator.run(state2, shots=m2_s).result()
        array_ionq = result2.measurements.reshape(1,m2_s*n2_q)

        return array_ionq, array_rigetti

    elif device_type == 'on_demand':
        # quantum circuit for generating weakly random bit string one (simulate Rigetti source)
        n1_q = 1 # alternatively run multiple qubits in parallel
        m1_s = int(math.ceil(n/n1_q))
        state1 = hadamard_circuit(n1_q)
        result1 = simulator.run(state1, shots=m1_s).result()
        array_rigetti = result1.measurements.reshape(1,m1_s*n1_q)

        # quantum circuit for generating weakly random bit string two (simulate IonQ source)
        n2_q = 1 # alternatively run multiple qubits in parallel
        m2_s = int(math.ceil(n/n2_q))
        state2 = hadamard_circuit(n2_q)
        result2 = simulator.run(state2, shots=m2_s).result()
        array_ionq = result2.measurements.reshape(1,m2_s*n2_q)

        return array_ionq, array_rigetti

