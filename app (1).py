{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "e4042bbe-f7a2-4b02-b066-822a43f1df86",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Overwriting app.py\n"
     ]
    }
   ],
   "source": [
    "%%writefile app.py\n",
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import joblib\n",
    "import os\n",
    "\n",
    "# Professional Title\n",
    "st.title(\"🏥 MedOps AI: Inventory Optimizer\")\n",
    "\n",
    "# Sidebar for Payments\n",
    "with st.sidebar:\n",
    "    st.header(\"💎 MedOps Pro\")\n",
    "    st.image(\"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa=YOUR_UPI_ID@okaxis&pn=MedOpsAI&am=499&cu=INR\")\n",
    "    st.caption(\"Upgrade for ₹499/mo to unlock Pro features\")\n",
    "\n",
    "# Load AI Brain\n",
    "MODEL_FILE = 'med_inventory_model.pkl'\n",
    "if os.path.exists(MODEL_FILE):\n",
    "    model = joblib.load(MODEL_FILE)\n",
    "    stock = st.number_input(\"Current Stock\", min_value=0, value=100)\n",
    "    flu_rate = st.slider(\"Regional Flu Rate (%)\", 0, 100, 15)\n",
    "    \n",
    "    if st.button(\"Generate Forecast\"):\n",
    "        prediction = model.predict([[stock, flu_rate]])[0]\n",
    "        st.success(f\"Predicted Demand: {int(prediction)} units\")\n",
    "else:\n",
    "    st.error(\"Model file not found. Please train and save the model first.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "72748264-8d14-439f-aeca-87ae0e8d8413",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.14.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
