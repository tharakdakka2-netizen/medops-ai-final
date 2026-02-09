import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# --- 1. DEFINE CUSTOM CLASSES ---
# This class must be defined here for joblib to load your pipeline.
class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def _init_(self, add_bedrooms_per_room=True):
        self.add_bedrooms_per_room = add_bedrooms_per_room
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        # Index positions based on California Housing dataset columns
        rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

# --- 2. LOAD THE MODEL ---
# Make sure "model.joblib" is uploaded to your GitHub in the same folder as app.py
try:
    model = joblib.load("model.joblib") 
except Exception as e:
    st.error(f"Error loading model: {e}")

# --- 3. STREAMLIT UI ---
st.title("California Housing Price Predictor")
st.write("Enter the details to estimate the median house value.")

# [span_2](start_span)Create input fields matching your technical experience project[span_2](end_span)
longitude = st.number_input("Longitude", value=-121.89)
latitude = st.number_input("Latitude", value=37.29)
housing_median_age = st.number_input("Housing Median Age", value=41.0)
total_rooms = st.number_input("Total Rooms", value=880.0)
total_bedrooms = st.number_input("Total Bedrooms", value=129.0)
population = st.number_input("Population", value=322.0)
households = st.number_input("Households", value=126.0)
median_income = st.number_input("Median Income", value=8.32)

# Prepare data for prediction
input_data = pd.DataFrame([[
    longitude, latitude, housing_median_age, total_rooms, 
    total_bedrooms, population, households, median_income
]], columns=[
    'longitude', 'latitude', 'housing_median_age', 'total_rooms', 
    'total_bedrooms', 'population', 'households', 'median_income'
])

if st.button("Predict Price"):
    prediction = model.predict(input_data)
    # [span_3](start_span)Highlight the result to showcase your 12% RMSE improvement[span_3](end_span)
    st.success(f"Estimated House Value: ${prediction[0]:,.2f}")
