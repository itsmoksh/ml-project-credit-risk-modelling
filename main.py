import streamlit as st
from backend.prediction import calc_risk
# Set the page configuration and title
st.set_page_config(page_title="Lauki Finance: Credit Risk Modelling", page_icon="📊")
st.title("Credit Risk Modelling")

# Create rows of three columns each
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# Assign inputs to the first row with default values
with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28)
with row1[1]:
    income = st.number_input('Income', min_value=0, value=1200000)
with row1[2]:
    loan_amount = st.number_input('Loan Amount', min_value=0, value=2560000)

# Calculate Loan to Income Ratio and display it
loan_to_income = loan_amount / income if income > 0 else 0
with row2[0]:
    st.text("Loan to Income Ratio:")
    st.text(f"{loan_to_income:.2f}")  # Display as a text field

# Assign inputs to the remaining controls
with row2[1]:
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
with row2[2]:
    average_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20)

with row3[0]:
    delinquency_ratio = st.number_input('Delinquency Ratio', min_value=0, max_value=100, step=1, value=30)
with row3[1]:
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio', min_value=0, max_value=100, step=1, value=30)
with row3[2]:
    number_of_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)


with row4[0]:
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
with row4[1]:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
with row4[2]:
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

received_columns= {
    'age': age,
    'loan_to_income': loan_to_income,
    'loan_tenure_months': loan_tenure_months,
    'average_dpd_per_delinquency': average_dpd_per_delinquency,
    'delinquency_ratio': delinquency_ratio,
    'credit_utilization_ratio': credit_utilization_ratio,
    'number_of_open_accounts': number_of_open_accounts,
    'residence_type': residence_type,
    'loan_purpose': loan_purpose,
    'loan_type': loan_type
}

if st.button('Calculate Risk'):
    score,credit_score,rate = calc_risk(received_columns)
    st.write(f"Default Probability: {score*100:.2f}%")
    st.write(f"Credict Score: {credit_score}")
    st.write(f"Rating: {rate}")
