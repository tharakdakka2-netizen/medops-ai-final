import streamlit as st
import pandas as pd
import joblib
import os

# Page Config
st.set_page_config(page_title="MedOps AI | Inventory Optimizer", layout="wide")
st.title("🏥 MedOps AI: Inventory Optimizer")

# Sidebar with your UPI ID
with st.sidebar:
    st.header("💎 MedOps Pro")
    plan = st.radio("Select Plan:", ["Free", "Pro (₹499/mo)"])
    
    if plan == "Pro (₹499/mo)":
        st.success("✅ Pro Features Active")
    else:
        st.info("Scan to unlock AI Restock Advice:")
        my_upi = "dakkatharakanth@ybl" 
        upi_url = f"upi://pay?pa={my_upi}&pn=MedOpsAI&am=499&cu=INR"
        qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={upi_url}"
        st.image(qr_api)
        st.caption("Pay via GPay, PhonePe, or Paytm")

# AI Logic
MODEL_FILE = 'med_inventory_model.pkl'

if os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Pharmacy Data")
            stock = st.number_input("Current Stock (Units)", min_value=0, value=100)
            flu_rate = st.slider("Regional Flu Rate (%)", 0, 100, 10)
            
        if st.button("Generate AI Forecast", type="primary"):
            # Predict using exactly 2 features to avoid 'Error 10'
            prediction = model.predict([[stock, flu_rate]])[0]
            with col2:
                st.subheader("💡 AI Result")
                st.metric("Predicted Demand", f"{int(prediction)} Units")
                if plan == "Pro (₹499/mo)":
                    order_qty = max(0, int(prediction) - stock)
                    st.metric("Suggested Restock", f"{order_qty} Units")
                else:
                    st.warning("Upgrade to Pro to see Restock Advice.")
    except Exception as e:
        st.error(f"Error: {e}. Please re-upload med_inventory_model.pkl")
else:
    st.error("Model file not found on GitHub.")
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
    color = 'red' if val < 30 else 'white'
    return f'color: {color}'

# Apply styling to the "Days Left" column
st.table(expiry_data.style.applymap(color_expiry, subset=['Days Left']))
import pandas as pd
from datetime import datetime
import os
import streamlit as st

# TRACKING LOGIC
def log_user_activity(email):
    log_file = "user_log.csv"
    new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email]], columns=["Timestamp", "Email"])
    if not os.path.isfile(log_file):
        new_data.to_csv(log_file, index=False)
    else:
        new_data.to_csv(log_file, mode='a', header=False, index=False)

# ADMIN PANEL (Visible only to you)
if st.session_state.get('user_email') == "your_email@gmail.com":
    with st.sidebar:
        if st.button("📊 Admin Dashboard"):
            st.write("### Total Logins:", pd.read_csv("user_log.csv").shape[0])
            st.write("### Unique Users:", pd.read_csv("user_log.csv")['Email'].nunique())

import os, pandas as pd, smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta

def run_expiry_check():
    df = pd.read_csv("master_inventory.csv")
    target_date = datetime.now().date() + timedelta(days=15)
    expiring = df[pd.to_datetime(df['Expiry']).dt.date == target_date]

    for _, row in expiring.iterrows():
        msg = EmailMessage()
        msg['Subject'] = f"⚠️ Expiry Alert: {row['Medicine Name']}"
        msg['From'] = os.environ.get("EMAIL_USER")
        msg['To'] = row['Customer Email']
        # HTML Template from our previous discussion goes here
        msg.set_content(f"Item {row['Medicine Name']} expires in 15 days.")
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
            smtp.send_message(msg)

    if __name__ == "__main__":
        run_expiry_check()

import pandas as pd
from datetime import datetime
import os
import streamlit as st

# TRACKING LOGIC
def log_user_activity(email):
    log_file = "user_log.csv"
    new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email]], columns=["Timestamp", "Email"])
    if not os.path.isfile(log_file):
        new_data.to_csv(log_file, index=False)
    else:
        new_data.to_csv(log_file, mode='a', header=False, index=False)

# ADMIN PANEL (Visible only to you)
if st.session_state.get('user_email') == "your_email@gmail.com":
    with st.sidebar:
        if st.button("📊 Admin Dashboard"):
            st.write("### Total Logins:", pd.read_csv("user_log.csv").shape[0])
            st.write("### Unique Users:", pd.read_csv("user_log.csv")['Email'].nunique())

from twilio.rest import Client
import os

def send_whatsapp_expiry_alert(customer_phone, medicine_name, expiry_date):
    # These are stored in your GitHub Secrets for safety
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    # Format the message for an Indian Pharmacist
    message_text = (
        f"🚨 MedOps AI: Expiry Alert\n\n"
        f"Namaste Sir, your stock of {medicine_name} is expiring on {expiry_date}.\n\n"
        f"💡 AI Suggestion: Move this batch to the front shelf and offer a 10% discount to clear stock today.\n\n"
        f"Click below to manage your inventory:\n"
        f"https://medopsai.streamlit.app"
    )

    message = client.messages.create(
        from_='whatsapp:+14155238886', # Your Twilio sandbox or business number
        body=message_text,
        to=f'whatsapp:+91{customer_phone}' # Dynamic Indian phone number
    )
    
    return message.sid

import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import os

# This script assumes you store your master inventory data in a CSV or Database
def run_expiry_check():
    # 1. Load your master database (e.g., from a private URL or GitHub)
    # For now, we'll assume a CSV named 'master_inventory.csv'
    if not os.path.exists("master_inventory.csv"):
        return

    df = pd.read_csv("master_inventory.csv")
    df['Expiry'] = pd.to_datetime(df['Expiry']).dt.date
    
    target_date = datetime.now().date() + timedelta(days=15)
    expiring_items = df[df['Expiry'] == target_date]

    if expiring_items.empty:
        print("No items expiring in 15 days.")
        return

    # 2. Email Setup (Using Secrets)
    ADMIN_EMAIL = os.environ.get("EMAIL_USER")
    ADMIN_PASS = os.environ.get("EMAIL_PASS")

    for _, row in expiring_items.iterrows():
        msg = EmailMessage()
        msg.set_content(f"Alert: {row['Medicine Name']} expires on {row['Expiry']}. Move to front shelf!")
        msg['Subject'] = f"⚠️ 15-Day Expiry Alert: {row['Medicine Name']}"
        msg['From'] = ADMIN_EMAIL
        msg['To'] = row['Customer Email']

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(ADMIN_EMAIL, ADMIN_PASS)
            smtp.send_message(msg)
            print(f"Sent alert for {row['Medicine Name']} to {row['Customer Email']}")

if _name_ == "_main_":
    run_expiry_check()
    
