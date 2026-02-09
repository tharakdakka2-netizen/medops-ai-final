import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# --- 1. DEFINE CUSTOM CLASSES ---
# You must include this because joblib needs the class definition 
# to "unpickle" your model successfully.
class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def _init_(self, add_bedrooms_per_room=True):
        self.add_bedrooms_per_room = add_bedrooms_per_room
        
    def fit(self, X, y=None):
        return self # Nothing to do
        
    def transform(self, X):
        # Assuming index positions based on the California Housing dataset
        rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

# --- 2. LOAD THE MODEL ---
# Ensure 'model.joblib' is in the same folder as this app.py in GitHub
try:
    [span_5](start_span)model = joblib.load("model.joblib") # Or your specific filename[span_5](end_span)
except Exception as e:
    st.error(f"Error loading model: {e}")

# --- 3. STREAMLIT UI ---
st.title("California Housing Price Predictor")
st.write("Enter the details to estimate the median house value.")

# [span_6](start_span)Create input fields for the user[span_6](end_span)
longitude = st.number_input("Longitude", value=-121.89)
latitude = st.number_input("Latitude", value=37.29)
housing_median_age = st.number_input("Housing Median Age", value=41.0)
total_rooms = st.number_input("Total Rooms", value=880.0)
total_bedrooms = st.number_input("Total Bedrooms", value=129.0)
population = st.number_input("Population", value=322.0)
households = st.number_input("Households", value=126.0)
median_income = st.number_input("Median Income", value=8.32)

# Convert inputs to a DataFrame for the pipeline
input_data = pd.DataFrame([[
    longitude, latitude, housing_median_age, total_rooms, 
    total_bedrooms, population, households, median_income
]], columns=[
    'longitude', 'latitude', 'housing_median_age', 'total_rooms', 
    'total_bedrooms', 'population', 'households', 'median_income'
])

if st.button("Predict Price"):
    prediction = model.predict(input_data)
    st.success(f"Estimated House Value: ${prediction[0]:,.2f}"
