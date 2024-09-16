import streamlit as st
import numpy_financial as npf
import pandas as pd
import altair as alt

# Set page title
st.title("Mortgage Calculator")

# First Row (3 columns for Amount borrowed, Interest rate, and Loan length)
col1, col2, col3 = st.columns(3)

with col1:
    amount_borrowed = st.number_input("Amount borrowed:", min_value=0, value=485000)

with col2:
    interest_rate = st.number_input("Interest rate:", min_value=0.0, value=6.28, format="%.2f")

with col3:
    loan_years = st.number_input("Length of loan (years):", min_value=1, value=25)

# Second Row (3 columns for Repayment frequency, Fees, and Fees frequency)
col4, col5, col6 = st.columns(3)

with col4:
    repayment_frequency = st.selectbox("Repayment frequency:", ["Monthly", "Fortnightly", "Weekly"])

with col5:
    fees = st.number_input("Fees:", min_value=0, value=10)

with col6:
    fees_frequency = st.selectbox("Fees frequency:", ["Monthly", "Annually"])


# Calculate repayment frequency and monthly interest rate
st.subheader("Your repayments")

monthly_interest_rate = (interest_rate / 100) / 12

if repayment_frequency == "Monthly":
    n_payments = loan_years * 12
elif repayment_frequency == "Fortnightly":
    n_payments = loan_years * 26
    monthly_interest_rate /= 2
elif repayment_frequency == "Weekly":
    n_payments = loan_years * 52
    monthly_interest_rate /= 4

# Calculate mortgage repayment using numpy_financial.pmt
if monthly_interest_rate > 0:
    repayment = npf.pmt(monthly_interest_rate, n_payments, -amount_borrowed)
else:
    repayment = amount_borrowed / n_payments

# Include fees in the repayment calculation
if fees_frequency == "Monthly":
    total_repayment = repayment + fees
elif fees_frequency == "Annually":
    total_repayment = repayment + (fees / 12)

# Display repayment details in a column layout with highlighted text
col7, col8, col9 = st.columns(3)

with col7:
    st.markdown(f"""
    <div style="background-color:#F0F8FF; padding:10px; border-radius:5px; text-align:center;">
        <h3 style="color:#0044cc;">Repayment Amount</h3>
        <p style="font-size:20px; font-weight:bold; color:#0044cc;">${total_repayment:,.2f} per {repayment_frequency.lower()}</p>
    </div>
    """, unsafe_allow_html=True)

# Calculate total repayments and interest
total_cost = total_repayment * n_payments
total_interest = total_cost - amount_borrowed

with col8:
    st.markdown(f"""
    <div style="background-color:#FAFAD2; padding:10px; border-radius:5px; text-align:center;">
        <h3 style="color:#B8860B;">Total Repayments</h3>
        <p style="font-size:20px; font-weight:bold; color:#B8860B;">${total_cost:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with col9:
    st.markdown(f"""
    <div style="background-color:#FFE4E1; padding:10px; border-radius:5px; text-align:center;">
        <h3 style="color:#DC143C;">Total Interest Paid</h3>
        <p style="font-size:20px; font-weight:bold; color:#DC143C;">${total_interest:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

# Create DataFrame for graph
months = list(range(1, n_payments + 1))
principal_paid = [npf.ppmt(monthly_interest_rate, month, n_payments, -amount_borrowed) for month in months]
interest_paid = [npf.ipmt(monthly_interest_rate, month, n_payments, -amount_borrowed) for month in months]
total_paid = [p + i for p, i in zip(principal_paid, interest_paid)]

df = pd.DataFrame({
    'Month': months,
    'Principal Paid': principal_paid,
    'Interest Paid': interest_paid,
    'Total Paid': total_paid
})

# Display graph based on user choice
st.subheader("Repayment Over Time")
# Graph type selector in a single row (full width)
col10, _ = st.columns([1, 2])  # Use two columns, with the first column taking the selector
with col10:
    graph_type = st.radio("Select graph type:", ["Bar", "Line"], horizontal=True)


if graph_type == "Bar":
    bar_chart = alt.Chart(df).transform_fold(
        ['Principal Paid', 'Interest Paid'],
        as_=['Type', 'Amount']
    ).mark_bar().encode(
        x='Month:Q',
        y='Amount:Q',
        color='Type:N'
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(bar_chart)

elif graph_type == "Line":
    line_chart = alt.Chart(df).transform_fold(
        ['Principal Paid', 'Interest Paid'],
        as_=['Type', 'Amount']
    ).mark_line().encode(
        x='Month:Q',
        y='Amount:Q',
        color='Type:N'
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(line_chart)
    
# Data for stacked bar chart
df1 = pd.DataFrame({
    'Category': ['Mortgage Details', 'Alternative'],
    'Principal': [amount_borrowed, amount_borrowed],  # Use the same principal for both bars
    'Interest': [total_interest, total_interest * 0.98],  # Example: Alternative option with lower interest
    'Total Repayment': [total_cost, total_cost * 0.98]  # Example: Alternative repayment slightly lower
})

# Stacked bar chart to resemble the example image
base = alt.Chart(df1).transform_fold(
    ['Principal', 'Interest'],
    as_=['Type', 'Amount']
).mark_bar().encode(
    x=alt.X('Category:N', title=''),
    y=alt.Y('sum(Amount):Q', title='Total Repayment ($)'),
    color=alt.Color('Type:N', scale=alt.Scale(domain=['Principal', 'Interest'], range=['#4169E1', '#87CEFA'])),
).properties(
    width=500,
    height=400
)

# Add text annotations at the top of each bar
text = base.mark_text(
    align='center',
    baseline='bottom',
    dx=0, dy=-5,  # Positioning of text
    color='black'
).encode(
    text=alt.Text('sum(Amount):Q', format='$,.0f')
)

st.altair_chart(base + text)