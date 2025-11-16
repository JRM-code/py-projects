import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 

st.title("Streamlit GUI functions")

# --- FUNCTION TO GET USER INPUT AND ADD NUMBERS --- #
num1 = st.number_input("Choose a number")

def add_me(num1):
    num2 = num1
    return num2

if st.button("Show me the number"):
    num2 = add_me(num1)
    st.write(num2)
