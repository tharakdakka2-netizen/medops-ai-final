import streamlit as st
import pandas as pd
import joblib
import os

# 1. Page Setup
st.set_page_config(page_title="MedOps AI | India", layout="wide")
st.title("🏥 MedOps AI: Inventory Optimizer")

# 2. Sidebar with UPI for Monetization
with st.sidebar:
    st.header("💎 MedOps Pro")
    plan = st.radio("Select Plan:", ["Free", "Pro (₹499/mo)"])
    if plan == "Pro (₹499/mo)":
        st.success("✅ Pro Features Unlocked")
    else:
        st.info("Scan to unlock AI Restock Advice:")
        # Placeholder UPI QR Code
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa=YOUR_UPI_ID@okaxis&pn=MedOpsAI&am=499&cu=INR")
        st.caption("Pay via GPay, PhonePe, or Paytm")

# 3. Model Loading and Prediction
MODEL_FILE = 'med_inventory_model.pkl'

if os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Inventory Data")
            stock = st.number_input("Current Stock Level", min_value=0, value=100)
            flu_rate = st.slider("Regional Infection Rate (%)", 0, 100, 10)
            
        if st.button("Generate AI Forecast", type="primary"):
            prediction = model.predict([[stock, flu_rate]])[0]
            
            with col2:
                st.subheader("AI Results")
                st.metric("Predicted Demand", f"{int(prediction)} Units")
                
                if plan == "Pro (₹499/mo)":
                    # Pro logic: Suggested order is demand minus current stock
                    order_qty = max(0, int(prediction * 1.1) - stock)
                    st.metric("Suggested Order", f"{order_qty} Units")
                else:
                    st.warning("Upgrade to Pro to see suggested order quantity.")
    except Exception as e:
        st.error(f"Error loading model: {e}. Please re-upload med_inventory_model.pkl")
else:
    st.error("Model file (med_inventory_model.pkl) not found. Please upload it to GitHub.")
