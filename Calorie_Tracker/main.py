import streamlit as st
from database import get_database, DatabaseSchema
from utils import SessionManager

# Page configuration
st.set_page_config(
    page_title="Calorie Cam",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on app start
db = get_database()
try:
    DatabaseSchema.initialize_database(db)
except Exception:
    pass  # Database already initialized

# Main app title
st.title("Calorie Cam")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    
    if SessionManager.is_authenticated():
        user = SessionManager.get_user()
        st.success(f"Logged in as: {user.username}")
        
        st.divider()
        
        if st.button("User Profile"):
            st.switch_page("pages/2_User_Info.py")
        
        if st.button("Log Calories"):
            st.switch_page("pages/3_Log_Calories.py")
        
        if st.button("Logout"):
            SessionManager.logout()
            st.rerun()
    else:
        st.info("Please log in to continue")
        if st.button("Go to Login"):
            st.switch_page("pages/1_Login.py")

st.divider()

# Main content

st.subheader("Welcome!")
st.write(
        """
        This app helps you track calories from food images.
        
        **Features:**
        - Upload food images for calorie analysis
        - Extract calories from nutritional labels
        - Manual calorie logging
        - Track your nutrition over time
        
        Use the navigation buttons on the left to get started.
        """
    )
if st.button("Get Started"):
     if SessionManager.is_authenticated():
        st.switch_page("pages/3_Log_Calories.py")
     else:
        st.switch_page("pages/1_Login.py")
