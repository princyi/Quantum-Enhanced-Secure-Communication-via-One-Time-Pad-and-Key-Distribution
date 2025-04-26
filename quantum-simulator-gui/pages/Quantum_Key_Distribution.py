import streamlit as st
import time
import numpy as np
import math
import time
from streamlit import components
from src import key_distribution, random_key_generator
from qiskit.visualization import visualize_transition

placeholder = st.empty()
random_bits = None
bases = None
key_length = 50

# st.set_page_config(page_title="Quantum Random Key Generation", page_icon="📈")
send_key = None

if 'submitted' not in st.session_state:
    st.session_state.submitted = False


# st.session_state

def record_submitted():
    st.session_state.submitted = True


def reset():
    st.session_state.submitted = False


def alice_bob(encoded_qubits, alice_bits, alice_bases):
    QUANTUM_CHANNEL = encoded_qubits
    st.write("Let's now generate random bases for Bob...")
    bob_bases = key_distribution.generate_random_bases(key_length)
    bob_bases_list = [i for i in bob_bases]
    st.write("The random output bases for Bob are:", bob_bases_list)
    qubits_received = QUANTUM_CHANNEL
    if st.spinner("Measuring Qubits received through Quantum Channel..."):
        time.sleep(2)
        bob_bits = key_distribution.measure(qubits_received, bob_bases)

    st.write("Bits received by Bob:", bob_bits)

    st.write("Now comes the verification part. Alice announces the bases she used over Classical Channel")

    CLASSICAL_CHANNEL = alice_bases

    st.write("Both Bob and Alice only keep the bases they share in common...")

    # Store the indices of the bases they share in common
    common_bases = [i for i in range(key_length) if CLASSICAL_CHANNEL[i] == bob_bases[i]]
    st.write("The indices of the first 10 bases they share in common are: " + str(common_bases[:10]))
    cols = st.columns(2)
    cols[0].write([i for i in alice_bases])
    cols[1].write([i for i in bob_bases])

    st.write("They both now exchange their common bases and discard the uncommon ones.")
    bob_bits = [int(bob_bits[index]) for index in common_bases]
    alice_bits = [int(alice_bits[0][index]) for index in common_bases]  # Alice keeps only the bits shared in common
    st.text("Since Alice and Bob are only keeping the bits measured in the bases they shared in common, "
            "they should have the same bits. To make sure this is the case, Alice will announce the first "
            "few bits that she has, and Bob should have the same ones. Of course, if Eve were trying to "
            "eavesdrop, she would also hear these first few bits, so Alice and Bob would have to discard "
            "them as well (after comparing to make sure they're the same as what they expect).")

    st.write("First 10 bits of Alice:", alice_bits[:10])
    st.write("Second 10 bits of Bob:", bob_bits[:10])
    if alice_bits[:10] == bob_bits[:10]:
        st.write("Yep, Alice and Bob seem to have the same bits!")
    else:
        st.write("Uh oh, at least one of the bits is different.")

    st.write("Since they publicly announced their first 10 bits, they have to be discarded.")
    st.write("The final remaining key with both of them are:")
    cols = st.columns(2)
    cols[0].write([i for i in alice_bits[10:]])
    cols[1].write([i for i in bob_bits[10:]])
    submitted = st.form_submit_button("Clear", on_click=record_submitted)


def alice_bob_eve(encoded_qubits, alice_bits, alice_bases):
    QUANTUM_CHANNEL = encoded_qubits
    qubits_intercepted = QUANTUM_CHANNEL
    st.write("This time, the qubits are intercepted by 😈 Eve...")
    eve_bases = key_distribution.generate_random_bases(key_length)  # Generate a random set of bases
    eve_bits = key_distribution.measure(qubits_intercepted, eve_bases)  # Measure the qubits
    st.write("Bases and Bits intercepted by Eve:")
    cols = st.columns(2)
    cols[0].write([i for i in eve_bases])
    cols[1].write([i for i in eve_bits])

    st.write("""Because of the No-Cloning Theorem of Quantum Mechanics, Eve cannot just copy the qubits over 
                from the quantum channel. Thus, Bob will never receive the qubits, making it obvious to him and Alice that 
                their message was intercepted. To prevent them from realizing what has happened, Eve must create her own 
                decoy qubits to send to Bob.""")

    print(eve_bits)
    # Eve encodes her decoy qubits and sends them along the quantum channel
    QUANTUM_CHANNEL, qc = key_distribution.encode(eve_bits, eve_bases)
    st.write("Tampered Encoded Qubits (by Eve):")
    for i in range(0, 5):
        st.write(QUANTUM_CHANNEL[i].draw(output='mpl', scale=0.5))

    st.write("The tampered Qubits now is being received by Bob. Unbeknownst, he carries on with his usual "
             "procedure:")
    st.write("Random bases for Bob...")
    bob_bases = key_distribution.generate_random_bases(key_length)
    bob_bases_list = [i for i in bob_bases]
    st.write("The random output bases for Bob are:", bob_bases_list)
    qubits_received = QUANTUM_CHANNEL
    if st.spinner("Measuring Qubits received through Quantum Channel..."):
        time.sleep(2)
        bob_bits = key_distribution.measure(qubits_received, bob_bases)

    st.write("Bits received by Bob:", bob_bits)

    st.write("Again Alice announces her bases she chose to encode her qubits in.")
    CLASSICAL_CHANNEL = alice_bases  # Alice tells Bob which bases she used

    # Store the indices of the bases they share in common
    st.write("Bob and Alice again only keep the bits corresponding to their common bases and discard the rest.")
    common_bases = [i for i in range(key_length) if CLASSICAL_CHANNEL[i] == bob_bases[i]]

    CLASSICAL_CHANNEL = common_bases  # Bob tells Alice which bases they shared in common
    bob_bits = [int(bob_bits[index]) for index in common_bases]
    alice_bits = [int(alice_bits[0][index]) for index in common_bases]  # Alice keeps only bits shared in common

    st.write("Now to verify, they both share their first 3 bits:")
    st.write("First 10 bits of Alice:", alice_bits[:10])
    st.write("Second 10 bits of Bob:", bob_bits[:10])
    if alice_bits[:10] == bob_bits[:10]:
        st.write("Yep, Alice and Bob seem to have the same bits!")
    else:
        st.write("Uh oh, at least one of the bits is different.")
    st.write("As you can see the keys remaining key received by Bob and Alice also wouldn't match:")
    cols = st.columns(2)
    cols[0].write([i for i in alice_bits[10:]])
    cols[1].write([i for i in bob_bits[10:]])
    submitted = st.form_submit_button("Clear", on_click=record_submitted)


def main():
    st.write("Click to generate random strings of bits...")
    submitted = st.button("Generate")
    with st.form("Key generation:"):
        random_key_generator.setup_devices('classical_gate')
        power = 10
        eps = 10 ** (-power)
        m = key_length
        n = math.floor((m - 1 - 2 * math.log2(eps)) / (1 + 1 - 1))
        array_1, array_2 = random_key_generator.create_quantum_circuit(n)
        alice_bits = random_key_generator.toeplitz_constructor(array_1, array_2, m, n)
        st.write(alice_bits)
        st.write("""Alice randomly chooses a basis of each bit (either the Z-basis or the X-basis). She can do this by flipping 
                    a coin and mapping each landing (heads or tails) with either one of the basis. But for our use case we are using a random
                    number generator.""")
        if st.spinner("Generating random bases for our random bit..."):
            time.sleep(2)
            bases = key_distribution.generate_random_bases(key_length)

        bases_list = [i for i in bases]
        st.write("The random output bits and bases are:", np.vstack((alice_bits, bases_list)))
        st.write("""Alice will now create a Quantum Circuit to encode each Qubit...""")
        if st.spinner("Encoding Qubit and creating Quantum Circuit"):
            time.sleep(1)
            encoded_qubits, qc = key_distribution.encode(alice_bits[0], bases)
        st.text("Encoded Qubits in Quantum Circuit (top 5):")
        for i in range(0, 5):
            st.write(encoded_qubits[i].draw(output='mpl', scale=0.5))
        st.write("Activate to let Eve intercept...")
        on = st.toggle("Intercept")
        st.write("Click to send the key")
        send = st.form_submit_button("Send")
        if send and on:
            alice_bob_eve(encoded_qubits, alice_bits, bases)
        elif send:
            alice_bob(encoded_qubits, alice_bits, bases)


main()
