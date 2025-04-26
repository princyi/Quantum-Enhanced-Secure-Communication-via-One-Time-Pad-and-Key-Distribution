import streamlit as st
import time
import numpy as np
import math
import time
from src import one_time_pad
from Crypto.Hash import HMAC, SHA512
from base64 import b64decode, b64encode
st.set_page_config(page_title="Quantum Random Key Generation", page_icon="📈")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False


#st.session_state

def record_submitted():
    st.session_state.submitted = True


def reset():
    st.session_state.submitted = False


option = st.selectbox(
    "Select an option",
    ("Encrypt Data", "Decrypt Data"),
    index=None,
    placeholder="Select an option...",
)

if option == "Encrypt Data":
    with st.form("Encrypt Data", clear_on_submit=True):
        reset()
        plaintext = st.text_area(key="plaintext_input", help='Enter your message to encrypt',
                                  label='Enter your message to encrypt. (Must be less than 1024 characters)')
        submitted = st.form_submit_button("Submit", on_click=record_submitted)

    if submitted:
        with st.form("Your encrypted data and Quantum Random Key", clear_on_submit=True):
            reset()
            with st.spinner("Generating Quantum Random Key..."):
                key = one_time_pad.generate_quantum_random_key(len(plaintext))
                #key = '12345'
                time.sleep(1)
            with st.spinner("Encrypting Data and Generating Hash..."):
                ciphertext, key = one_time_pad.encrypt(plaintext, key)
                h = HMAC.new(key.encode(), digestmod=SHA512)
                h.update(plaintext.encode())
                #ciphertext = 'hello'
                time.sleep(2)

            st.write("Your key:", key)
            st.write("Your Message Authentication Code is:", h.hexdigest())
            st.write("Your ciphertext:", ciphertext)

            submitted = st.form_submit_button("Destroy data", on_click=record_submitted)

if option == "Decrypt Data":
    with st.form("Decrypted data", clear_on_submit=True):
        reset()
        ciphertext = st.text_area(key="ciphertext_input", help='Enter your message to decrypt',
                                   label="Enter your message to decrypt")
        mac = st.text_area("Enter your Message Authenticated Code:")
        key = st.text_area(key="key_input", help='Enter your key', label='Enter your key')
        submitted = st.form_submit_button("Submit", on_click=record_submitted)

    if submitted:
        with st.form("Your decrypted data", clear_on_submit=True):
            reset()
            try:
                with st.spinner("Decrypting Data..."):
                    plaintext = one_time_pad.decrypt(ciphertext, key)
                    # ciphertext = 'decrypted data'
                    time.sleep(2)
                st.write("Verifying message authenticity...")
                h = HMAC.new(key.encode(), digestmod=SHA512)
                h.update(plaintext.encode())
                try:
                    h.hexverify(mac)
                    st.write("Message authentication successful")
                    st.write("Your plaintext:", plaintext)
                except ValueError:
                    st.write("The message or the key is wrong. Authentication failed.")

            except Exception as e:
                st.write("unable to decrypt message due to exception: ", e)

            submitted = st.form_submit_button("Destroy data", on_click=record_submitted)
