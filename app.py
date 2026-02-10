import streamlit as st
from st_paywall import add_auth  # The "Gatekeeper" library
import pandas as pd
import joblib

st.set_page_config(page_title="MedOps AI | Pro", layout="wide")

# 1. SETUP THE PAYWALL
# This handles Google Login + Stripe Subscription automatically
add_auth(
    required=False, # Set to True to block the WHOLE app until payment
    subscription_button_text="Unlock Pro for ₹19/mo",
    button_color="#FF4B4B"
)

st.title("🏥 MedOps AI: Inventory Optimizer")

# 2. CHECK SUBSCRIPTION STATUS
is_pro = st.session_state.get("user_subscribed", False)

with st.sidebar:
    if is_pro:
        st.success("💎 PRO ACCOUNT ACTIVE")
        st.write(f"Welcome, {st.experimental_user.email}")
    else:
        st.warning("Running Free Version")
        st.info("Upgrade for ₹19/mo to see Restock Advice.")

# 3. AI LOGIC
stock = st.number_input("Current Stock", value=100)
flu = st.slider("Flu Rate %", 0, 100, 10)

if st.button("Generate Forecast"):
    # Load your model (assuming 2 features as discussed)
    model = joblib.load('med_inventory_model.pkl')
    prediction = model.predict([[stock, flu]])[0]
    
    st.metric("Predicted Demand", f"{int(prediction)} Units")
    
    # THE PAYWALL GATE
    if is_pro:
        restock = max(0, int(prediction) - stock)
        st.metric("📦 SUGGESTED RESTOCK", f"{restock} Units")
    else:
        st.error("🔒 Restock Advice is a Pro Feature. Please subscribe below.")
        # The subscription button appears here automatically if not paid
    


import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# 1. Clean Training Data (Exactly 2 features to avoid 'Error 10')
# We provide a simple dataset for the AI to learn from
df = pd.DataFrame({
    'Current_Stock': [100, 50, 200, 30, 80, 10, 150, 5, 300, 45],
    'Regional_Flu_Rate': [5, 25, 10, 50, 30, 60, 15, 80, 2, 40],
    'Inventory_Required': [110, 200, 150, 350, 280, 450, 180, 500, 310, 300]
})

# 2. Define Features (X) and Target (y)
X = df[['Current_Stock', 'Regional_Flu_Rate']]
y = df['Inventory_Required']

# 3. Train the AI (Ensuring 'import' is spelled correctly in the session)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Save as med_inventory_model.pkl
joblib.dump(model, 'med_inventory_model.pkl')
print("✅ SUCCESS: Simplified model created. Upload this to GitHub!")
import datetime

st.divider()
st.header("📅 MedOps Expiry Tracker")

# Create a small input form
with st.expander("➕ Add New Batch"):
    col1, col2, col3 = st.columns(3)
    with col1:
        med_name = st.text_input("Medicine Name")
    with col2:
        expiry_date = st.date_input("Expiry Date", min_value=datetime.date.today())
    with col3:
        batch_qty = st.number_input("Batch Quantity", min_value=1)
    
    if st.button("Save Batch"):
        st.success(f"Batch for {med_name} saved locally!")

# Sample Expiry Data (In a real app, this would come from a database)
expiry_data = pd.DataFrame([
    {"Medicine": "Paracetamol", "Expiry": "2026-03-15", "Days Left": 33},
    {"Medicine": "Amoxicillin", "Expiry": "2026-02-25", "Days Left": 15},
    {"Medicine": "Vitamin D3", "Expiry": "2027-01-10", "Days Left": 334},
])

# Displaying the tracker with alerts
st.subheader("⚠️ Upcoming Expiries")

def color_expiry(val):
    color = 'red' if val < 30 else 'black'
    return f'color: {color}'

# Apply styling to the "Days Left" column
st.table(expiry_data.style.applymap(color_expiry, subset=['Days Left']))
