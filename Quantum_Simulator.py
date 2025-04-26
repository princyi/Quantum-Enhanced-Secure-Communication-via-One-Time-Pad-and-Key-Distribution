import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Quantum Cryptography Simulator! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Simulations available:
    1. Random Key Generation
    2. Quantum One Time Pad CryptoGraphy
    3. Quantum Key Distribution
"""
)