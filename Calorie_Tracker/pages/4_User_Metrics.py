"""Metrics page."""
import streamlit as st
from database import get_database, DatabaseSchema
from domain import User
from utils import SessionManager, PasswordManager, AuthValidator

user = SessionManager.get_user()
    
if user:
    st.write(f"Logged in as: **{user.username}**")
    # dummy data 
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

else:
    st.warning("Please log in first")
    st.switch_page("pages/1_Login.py")
