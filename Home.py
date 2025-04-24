import streamlit as st

st.set_page_config(
    page_title="House Buying Experiment",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome to House Buying Experiment")

st.write("""
## About This Application

This application simulates a house buying experiment with the following features:

1. **Manual Experiment Mode**
   - 5 buyers participate in 3 rounds
   - Each round has different budget constraints
   - Players can view and purchase properties

2. **Simulation Mode**
   - Automated simulation of buying behavior
   - Analysis of price distributions
   - Visualization of results

Please use the sidebar to navigate between pages.
""") 