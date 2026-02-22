"""Metrics page."""
import streamlit as st
from database import get_database, DatabaseSchema
from domain import User
from utils import SessionManager, PasswordManager, AuthValidator
import pandas as pd 

user = SessionManager.get_user()
    
if user:
    st.write(f"Logged in as: **{user.username}**")
    # dummy data 
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")
    
    # Fetch calorie entries for the logged-in user
    db = get_database()
    query = "SELECT * FROM calories WHERE user_id = ?"
    df = pd.read_sql_query(query, db.connection, params=(user.id,))
    rename_mapping = {
    'food_name': 'Food Name',
    'calories': 'Calories',
    'quantity': 'Quantity',
    'unit': 'Unit',
    'food_type': 'Food Type',
    'source': 'Source',
    'notes': 'Notes',
    'logged_at': 'Time Logged'
    }
    desired_columns = ["Food Name", "Calories", "Quantity", "Unit", "Food Type", "Source", "Notes", "Time Logged"]


    df = df.rename(columns=rename_mapping)
    st.dataframe(df[desired_columns])

else:
    st.warning("Please log in first")
    st.switch_page("pages/1_Login.py")