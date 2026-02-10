import streamlit as st
import pandas as pd
import joblib
import os

# 1. Page Configuration
st.set_page_config(page_title="MedOps AI | Inventory Optimizer", layout="wide")
st.title("🏥 MedOps AI: Inventory Optimizer")

# 2. Sidebar with YOUR UPI (dakkatharakanth@ybl)
with st.sidebar:
    st.header("💎 MedOps Pro")
    plan = st.radio("Select Plan:", ["Free", "Pro (₹499/mo)"])
    
    if plan == "Pro (₹499/mo)":
        st.success("✅ Pro Features Active")
    else:
        st.info("Scan to unlock AI Restock Advice:")
        # Your specific UPI ID is now integrated below
        my_upi = "dakkatharakanth@ybl" 
        upi_url = f"upi://pay?pa={my_upi}&pn=MedOpsAI&am=499&cu=INR"
        qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={upi_url}"
        st.image(qr_api)
        st.caption("Pay via GPay, PhonePe, or Paytm")

# 3. AI Prediction Logic
MODEL_FILE = 'med_inventory_model.pkl'

if os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Pharmacy Data")
            stock = st.number_input("Current Stock (Units)", min_value=0, value=100)
            flu_rate = st.slider("Regional Flu/Infection Rate (%)", 0, 100, 10)
            
        if st.button("Generate AI Forecast", type="primary"):
            # Ensure model input matches features used during training
            prediction = model.predict([[stock, flu_rate]])[0]
            
            with col2:
                st.subheader("💡 AI Result")
                st.metric("Predicted Demand", f"{int(prediction)} Units")
                
                if plan == "Pro (₹499/mo)":
                    # Suggested order = Predicted demand - Current stock
                    order_qty = max(0, int(prediction) - stock)
                    st.metric("Suggested Restock", f"{order_qty} Units")
                    st.write("✅ *Order logic calculated for Pro plan.*")
                else:
                    st.warning("Upgrade to Pro to see exact 'Suggested Restock' quantities.")
                    
    except Exception as e:
        st.error(f"Error loading model: {e}. Please ensure you uploaded a fresh .pkl file.")
else:
    st.error("Model file (med_inventory_model.pkl) not found on GitHub. Please upload it.")
                    
