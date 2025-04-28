import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
st.set_page_config(page_title="model 🚗", layout="wide")
@st.cache_data
def read():
    return pd.read_csv(r"datasets/EDa.csv")

df = read()

# Dashboard Title
st.title("Cars Price Prediction Model 🚗")

# --- Correct way to load the model ---
with open(r'data/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Directory containing all encoder files
encoder_dir = r'data'

# Dictionary to store encoders
encoders = {}

# List of encoder filenames
encoder_files = [
    'aspiration_encoder.pkl',
    'carbody_encoder.pkl',
    'CarName_encoder.pkl',
    'cylindernumber_encoder.pkl',
    'doornumber_encoder.pkl',
    'drivewheel_encoder.pkl',
    'enginelocation_encoder.pkl',
    'enginetype_encoder.pkl',
    'fuelsystem_encoder.pkl',
    'fueltype_encoder.pkl'
]

# Load each encoder properly
for encoder_file in encoder_files:
    file_path = os.path.join(encoder_dir, encoder_file)
    with open(file_path, 'rb') as f:
        encoder_name = encoder_file.replace('_encoder.pkl', '')  # Cleaner key
        encoders[encoder_name] = pickle.load(f)


col1,col2,col3=st.columns(3)
with col1:
    carname=st.selectbox("select car name",df['CarName'].unique())
    door=st.selectbox("select car doornumber",df['doornumber'].unique())
    body=st.selectbox("select car carbody",df['carbody'].unique())
    fuelsystem=st.selectbox("select car fuelsystem",df['fuelsystem'].unique())
    carlength=st.slider("carlength",df['carlength'].min(),df['carlength'].max())
    carwidth=st.slider("carwidth",df['carwidth'].min(),df['carwidth'].max())
    stroke=st.slider("stroke",df['stroke'].min(),df['stroke'].max())
    citympg=st.slider("citympg",df['citympg'].min(),df['citympg'].max())
    
with col2:
    fuel=st.selectbox("select car fueltype",df['fueltype'].unique())
    wheel=st.selectbox("select car drivewheel",df['drivewheel'].unique())
    englocation=st.selectbox("select car enginelocation",df['enginelocation'].unique())
    wheelbase=st.slider("wheelbase",df['wheelbase'].min(),df['wheelbase'].max())
    carheight=st.slider("carheight",df['carheight'].min(),df['carheight'].max())
    boreratio=st.slider("boreratio",df['boreratio'].min(),df['boreratio'].max())
    compressionratio=st.slider("compressionratio",df['compressionratio'].min(),df['compressionratio'].max())
    peakrpm=st.slider("peakrpm",df['peakrpm'].min(),df['peakrpm'].max())
    
with col3:
    aspirat=st.selectbox("select car aspiration",df['aspiration'].unique())
    cylindernumber=st.selectbox("select car cylindernumber",df['cylindernumber'].unique())
    enginetype=st.selectbox("select car enginetype",df['enginetype'].unique())
    symbol=st.slider("symboling",df['symboling'].min(),df['symboling'].max())
    curbweight=st.slider("curbweight",df['curbweight'].min(),df['curbweight'].max())
    enginesize=st.slider("enginesize",df['enginesize'].min(),df['enginesize'].max())
    horsepower=st.slider("horsepower",df['horsepower'].min(),df['horsepower'].max())
    highwaympg=st.slider("highwaympg",df['highwaympg'].min(),df['highwaympg'].max())
    

encoded_carname = encoders['CarName'].transform([carname])[0]
encoded_fueltype = encoders['fueltype'].transform([fuel])[0]
encoded_aspiration = encoders['aspiration'].transform([aspirat])[0]
encoded_doornumber = encoders['doornumber'].transform([door])[0]
encoded_carbody = encoders['carbody'].transform([body])[0]
encoded_drivewheel = encoders['drivewheel'].transform([wheel])[0]
encoded_enginelocation = encoders['enginelocation'].transform([englocation])[0]
encoded_enginetype = encoders['enginetype'].transform([enginetype])[0]
encoded_cylindernumber = encoders['cylindernumber'].transform([cylindernumber])[0]
encoded_fuelsystem = encoders['fuelsystem'].transform([fuelsystem])[0]


input_data = pd.DataFrame({
    'symboling': [symbol],
    'CarName': [encoded_carname],
    'fueltype': [encoded_fueltype],
    'aspiration': [encoded_aspiration],
    'doornumber': [encoded_doornumber],
    'carbody': [encoded_carbody],
    'drivewheel': [encoded_drivewheel],
    'enginelocation': [encoded_enginelocation],
    'wheelbase': [wheelbase],
    'carlength': [carlength],
    'carwidth': [carwidth],
    'carheight': [carheight],
    'curbweight': [curbweight],
    'enginetype': [encoded_enginetype],
    'cylindernumber': [encoded_cylindernumber],
    'enginesize': [enginesize],
    'fuelsystem': [encoded_fuelsystem],
    'boreratio': [boreratio],
    'stroke': [stroke],
    'compressionratio': [compressionratio],
    'horsepower': [horsepower],
    'peakrpm': [peakrpm],
    'citympg': [citympg],
    'highwaympg': [highwaympg]
})

if st.button('Predict Price'):
    prediction = model.predict(input_data)
    st.success(f"Predicted Car Price: {prediction[0]:,.2f}")
