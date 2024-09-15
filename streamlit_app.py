import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("My Mortgage Repayment Calculator")

st.write("### Input Data below:")
col1, col2 = st.columns(2)
home_val = col1.number_input("Home value", min_value=0, value=500000)
deposit_val = col1.number_input("Deposit", min_value=0, value=100000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value= 6.5)
loat_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)