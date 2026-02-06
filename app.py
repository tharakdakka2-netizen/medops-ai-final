import streamlit as st
import pandas as pd
import joblib
import os

st.title("🏥 MedOps AI: Inventory Optimizer")

# Load Model
MODEL_FILE = 'med_inventory_model.pkl'

if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)
    stock = st.number_input("Current Stock", min_value=0, value=100)
    flu_rate = st.slider("Flu Rate (%)", 0, 100, 10)
    
    if st.button("Generate Forecast"):
        prediction = model.predict([[stock, flu_rate]])[0]
        st.success(f"Predicted Demand: {int(prediction)} Units")
else:
    st.error("Model file missing! Please upload med_inventory_model.pkl to GitHub.")
