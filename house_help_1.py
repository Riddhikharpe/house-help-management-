# -*- coding: utf-8 -*-
"""house_help_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1y6VsS4bgDfzCIjTl8CFqOoExEgj2HXlQ
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configure file paths
EXCEL_FILE = 'house_helps.xlsx'
UPLOADS_DIR = 'uploads'

# User authentication
USER_CREDENTIALS = {"admin": "password123"}  # Simple dictionary for username and password

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Create Excel file if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=[
        'name', 'age', 'gender', 'address', 'contact',
        'experience', 'photo_path', 'rate', 'registration_date'
    ])
    df.to_excel(EXCEL_FILE, index=False)

# Function to register a helper
def register_helper():
    st.subheader("Register New Helper")

    # Get user inputs for helper registration
    name = st.text_input("Enter Name:")
    age = st.number_input("Enter Age:", min_value=18, max_value=100)
    gender = st.selectbox("Select Gender:", ['Male', 'Female', 'Other'])
    address = st.text_area("Enter Address:")
    contact = st.text_input("Enter Contact Number:")
    experience = st.number_input("Enter Experience (in years):", min_value=0)
    rate = st.number_input("Enter Rate per Hour:", min_value=0.0)

    # File uploader for photo
    photo = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"])

    # Handle form submission
    if st.button("Register Helper"):
        try:
            if photo is not None:
                photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.name}"
                photo_path = os.path.join(UPLOADS_DIR, photo_filename)
                with open(photo_path, "wb") as f:
                    f.write(photo.getbuffer())
            else:
                photo_path = "No photo uploaded"

            # Prepare data for Excel
            registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'name': name,
                'age': age,
                'gender': gender,
                'address': address,
                'contact': contact,
                'experience': experience,
                'rate': rate,
                'registration_date': registration_date,
                'photo_path': photo_path
            }

            # Read existing data
            df = pd.read_excel(EXCEL_FILE)

            # Append new data
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

            # Save back to Excel
            df.to_excel(EXCEL_FILE, index=False)

            st.success("Registration successful!")
        except Exception as e:
            st.error(f"Error during registration: {str(e)}")

# Function to search helpers by rate
def search_helpers():
    st.subheader("Search Helpers by Rate")

    # Get user input for max price filter
    max_price = st.number_input("Enter Max Rate to filter helpers:", min_value=0.0)

    # Display the filtered helpers
    if st.button("Search"):
        try:
            # Read Excel file
            df = pd.read_excel(EXCEL_FILE)

            # Filter by max price
            filtered_df = df[df['rate'] <= max_price]

            if filtered_df.empty:
                st.warning("No helpers found with the given criteria.")
            else:
                st.dataframe(filtered_df[['name', 'age', 'gender', 'rate']])
        except Exception as e:
            st.error(f"Error during search: {str(e)}")

# Function to handle Excel file download with authentication
def download_excel():
    st.subheader("Download Excel File")

    # Authentication
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success("Login successful!")
            st.markdown(f"[Click here to download the Excel file](/{EXCEL_FILE})")
        else:
            st.error("Invalid username or password")

# Main Streamlit UI
def main():
    st.title("House Helper Registration and Search")

    st.write("Welcome to the House Helper Registration and Search System.")

    # Buttons for navigation (one below the other)
    st.button("Register Helper", on_click=register_helper)
    st.button("Search Helpers", on_click=search_helpers)
    st.button("Download Excel File", on_click=download_excel)

# Run the app
if __name__ == '__main__':
    main()

