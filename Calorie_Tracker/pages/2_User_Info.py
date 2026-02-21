"""User information page."""
import streamlit as st
from datetime import datetime
from ..database import get_database
from ..domain import User
from ..utils import SessionManager


def main():
    """Main function for user information page."""
    SessionManager.require_authentication()(lambda: None)()
    
    st.title("User Information")
    
    user = SessionManager.get_user()
    
    if user:
        st.subheader(f"Welcome, {user.username}!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Profile Information")
            st.write(f"**Username:** {user.username}")
            st.write(f"**Email:** {user.email}")
        
        with col2:
            st.write("### Account Details")
            if user.created_at:
                st.write(f"**Member Since:** {user.created_at}")
            if user.updated_at:
                st.write(f"**Last Updated:** {user.updated_at}")
        
        st.divider()
        
        st.subheader("Update Profile")
        
        new_email = st.text_input("Email", value=user.email)
        new_password = st.text_input("New Password (leave blank to keep current)", type="password")
        
        if st.button("Update Profile"):
            # TODO: Update user in database
            st.success("Profile update functionality coming soon - database integration needed")
        
        st.divider()
        
        if st.button("Logout", key="logout_btn"):
            SessionManager.logout()
            st.success("Logged out successfully")
            st.rerun()
    else:
        st.warning("Please log in first")
        st.switch_page("pages/1_Login.py")


if __name__ == "__main__":
    main()
