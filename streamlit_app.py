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
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)


# Calculate the repayments
loan_amount = home_val - deposit_val
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repalyments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Month Replayments", value=f"{monthly_payment:,.2f}")
col2.metric(label="Total Replayments", value=f"{total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"{total_interest:,.0f}")