# -*- coding: utf-8 -*-
"""Loan_simulation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eqnTMeFLm3SoHsQ_mRh6dVwsK0AEo2xd
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# Page config
st.set_page_config(page_title="Loan Simulator", layout="centered")
st.title("💰 Loan Simulation App")

# Load and display a logo or image
image_path = "logo.png"  # Replace with your image filename
if os.path.exists(image_path):
    st.image(Image.open(image_path), width=150)

# Occupation options and rates
occupations = {
    "Fonctionnaire": 0.04,
    "Salarie": 0.05,
    "Travailleur": 0.06
}

# Input section
st.subheader("📋 Loan Inputs")
occu = st.selectbox("Select Occupation Type", list(occupations.keys()))
amount = st.number_input("Loan Amount (MAD)", min_value=1000, step=500)
duration = st.number_input("Duration (years)", min_value=1, step=1)
rate = occupations[occu]

# Simulation calculation
def calculate_loan(amount, years, rate):
    months = years * 12
    monthly_rate = rate / 12
    monthly_payment = (amount * monthly_rate) / (1 - (1 + monthly_rate) ** -months)
    total_payment = monthly_payment * months
    return round(monthly_payment, 2), round(total_payment, 2)

if st.button("Simulate Loan"):
    monthly, total = calculate_loan(amount, duration, rate)
    st.success(f"Monthly Payment: {monthly} MAD")
    st.info(f"Total Repayment over {duration} years: {total} MAD")

    # Save to Excel (local)
    history_file = "loan_history.xlsx"
    new_entry = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Occupation": occu,
        "Amount": amount,
        "Duration": duration,
        "Rate": f"{rate * 100}%",
        "Monthly Payment": monthly,
        "Total Payment": total
    }])

    if os.path.exists(history_file):
        old = pd.read_excel(history_file)
        df = pd.concat([old, new_entry], ignore_index=True)
    else:
        df = new_entry

    df.to_excel(history_file, index=False)
    st.success("Simulation saved to local history file: loan_history.xlsx")

# Show saved history
if os.path.exists("loan_history.xlsx"):
    with st.expander("📂 View Past Simulations"):
        hist_df = pd.read_excel("loan_history.xlsx")
        st.dataframe(hist_df)
