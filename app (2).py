%%writefile app.py
import streamlit as st
import pandas as pd
import joblib
import os

# 1. Branding
st.set_page_config(page_title="MedOps AI | India", layout="wide")
st.title("🏥 MedOps AI: Inventory Optimizer")

# 2. Sidebar & Payments
with st.sidebar:
    st.header("💎 Upgrade to Pro")
    plan = st.radio("Select Plan:", ["Free", "Pro (₹499/mo)"])
    if plan == "Pro (₹499/mo)":
        st.success("✅ Pro Features Active")
    else:
        st.info("Scan to unlock AI Restock Advice:")
        # UPI QR Code Generation
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa=YOUR_UPI_ID@okaxis&pn=MedOpsAI&am=499&cu=INR")

# 3. Prediction Engine
MODEL_FILE = 'med_inventory_model.pkl'

if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)
    
    col1, col2 = st.columns(2)
    with col1:
        stock = st.number_input("Current Stock", min_value=0, value=100)
        flu_rate = st.slider("Local Flu Rate (%)", 0, 100, 10)
        
    if st.button("Generate Forecast", type="primary"):
        prediction = model.predict([[stock, flu_rate]])[0]
        with col2:
            st.metric("Predicted Demand", f"{int(prediction)} Units")
            if plan == "Pro (₹499/mo)":
                order = max(0, int(prediction * 1.1) - stock)
                st.metric("Suggested Order", f"{order} Units")
            else:
                st.warning("Upgrade to see Order Quantity.")
else:
    st.error("Error: med_inventory_model.pkl not found. Please upload it to GitHub.")
