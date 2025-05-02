# -*- coding: utf-8 -*-
"""
Created on Fri May  2 15:41:54 2025

@author: swank
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import os


st.set_page_config(layout="wide")
    
st.image(os.path.join("images", "Atomic_Wines_Logo.png"), use_column_width=False)
st.caption("Generate jittered wine datasets for the Atomic Wines case study")

# Add space
st.markdown("")

# Instructional caption
st.caption("➡ Adjust the jitter factor slider below (if desired), then click **Generate Data** to create the datasets for download.")


# Jitter factor slider
factor = st.slider("Jitter Factor (%)", min_value=1, max_value=20, value=10)



# Define jitter function
def jitter(number, factor):
    percent = random.randint(1, factor) / 100
    sign = random.choice([-1, 1])
    return round(number + sign * number * percent, 3)

# Action button
if st.button("Generate Data"):
    
    
    # Get file paths relative to app folder
    selling_path = os.path.join("data", "Wines_Selling.csv")
    remain_path = os.path.join("data", "Wines_Remain.csv")
    
    # Read CSVs
    wines_selling = pd.read_csv(selling_path, encoding='latin-1')
    wines_remain = pd.read_csv(remain_path, encoding='latin-1')
    
    # Split ID/class from attributes
    selling_ID_class = wines_selling.iloc[:, 0:5]
    selling_attributes = wines_selling.iloc[:, 5:17]
    
    remain_ID_class = wines_remain.iloc[:, 0:4]
    remain_attributes = wines_remain.iloc[:, 4:16]
    
    # Shuffle attribute rows
    #selling_attributes = selling_attributes.sample(frac=1).reset_index(drop=True)
    #remain_attributes = remain_attributes.sample(frac=1).reset_index(drop=True)
    
    # Jitter chemical properties 
    for col in selling_attributes.columns:
        selling_attributes[col] = selling_attributes[col].apply(lambda x: jitter(x, factor))
    for col in remain_attributes.columns:
        remain_attributes[col] = remain_attributes[col].apply(lambda x: jitter(x, factor))
    
    # Recombine
    wines_sold = pd.concat([selling_ID_class, selling_attributes], axis=1)
    wines_remaining = pd.concat([remain_ID_class, remain_attributes], axis=1)
    
    # Display preview
    st.subheader("Jittered Wines Sold Data (preview)")
    st.write(wines_sold.head())
    
    st.subheader("Jittered Wines Remain Data (preview)")
    st.write(wines_remaining.head())
    
    # Prepare CSVs for download
    csv_sold = wines_sold.to_csv(index=False).encode('utf-8')
    csv_remain = wines_remaining.to_csv(index=False).encode('utf-8')
    
    st.download_button("Download Jittered Wines Sold CSV", data=csv_sold, file_name="Wines_Sold.csv", mime="text/csv")
    st.download_button("Download Jittered Wines Remain CSV", data=csv_remain, file_name="Wines_Remain.csv", mime="text/csv")