import streamlit as st
import time
import numpy as np
import math
import time
from src import random_key_generator

st.set_page_config(page_title="Quantum Random Key Generation", page_icon="📈")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

#st.session_state

def record_submitted():
    st.session_state.submitted = True

def reset():
    st.session_state.submitted = False


with st.form("Select device type", clear_on_submit=True):

    option = st.selectbox(
        "Select Quantum device type",
        ('Classical-gate', 'Quantum-gate')
    )
    print(option)
    if option == 'Classical-gate':
        device, simulator = random_key_generator.setup_devices('classical_gate')
    elif option == 'Quantum-gate':
        device, rigetti, ionq = random_key_generator.setup_devices('quantum_gate')

    submitted = st.form_submit_button("Submit", on_click=record_submitted)


with st.form("Configuration", clear_on_submit=True):
    reset()
    st.write("Select power of security parameter")
    power = st.slider("Security Parameter", 2, 8, help="Security parameter is any randomly picked numeber.", key='power_slider')
    eps = 10**(-power)
    m = st.slider("Desired random number length", 10, 50, key='random_number_length',
                  help='The length of random numbers. Due to hardware limitations, the max length is set to 50.')
    k_one = st.slider("Minimum entropy for first source", 0.1, 1.0, key='k_1')
    k_two = st.slider("Minimum entropy for first source", 0.1, 1.0, key='k_2')
    n = math.floor((m-1-2*math.log2(eps))/(k_one+k_two-1))
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit", on_click=record_submitted)

if submitted:
    array_1, array_2 = random_key_generator.create_quantum_circuit(n)
    # Uncomment to run on on_demand simulator or quantum gate
    # Commented because running on actual simulator takes as a lot of time and running it live may not be feasible.
    array_1, array_2 = random_key_generator.create_quantum_task('on_demand', array_1, array_2, n)
    reset()
    with st.form("Generating Quantum Circuit", clear_on_submit=True):
        st.write("Weakly random strings of bits of size:", array_1.shape)
        st.write("String 1:", str(array_1))
        st.write("String 2:", str(array_2))
        with st.spinner("Initializing toeplitz constructor"):
            res = random_key_generator.toeplitz_constructor(array_1, array_2, m, n)
            time.sleep(3)
        st.write(f"The {m} random output bits are:\n{res}.")
        st.form_submit_button("Clear", on_click=record_submitted)





