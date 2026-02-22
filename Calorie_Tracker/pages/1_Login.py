"""Login page."""
import streamlit as st
from database import get_database, DatabaseSchema
from domain import User
from utils import SessionManager, PasswordManager, AuthValidator

st.set_page_config(
    page_title="CalorieCam",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def show_login_form():
    st.title("CalorieCam")

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    #login mode
    if st.session_state.auth_mode == "login":
        st.subheader("Sign In")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                st.info("Login functionality coming soon")

        if st.button("Create Account"):
            st.session_state.auth_mode = "signup"
            st.rerun() #refresh page with switched mdoe

    #signup mode
    elif st.session_state.auth_mode == "signup":
        st.subheader("Create Account")

        new_username = st.text_input("New Username")
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            valid, msg = AuthValidator.validate_username(new_username)
            if not valid:
                st.error(msg)
            else:
                valid, msg = AuthValidator.validate_email(new_email)
                if not valid:
                    st.error(msg)
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    st.info("Sign up functionality to be added")

        if st.button("Back to Login"):
            st.session_state.auth_mode = "login" #switch back to login mode
            st.rerun()

def main():
    """Main function for login page."""
    # Initialize database
    db = get_database()
    try:
        DatabaseSchema.initialize_database(db)
    except Exception:
        pass  # Database already initialized
    
    # Check if already logged in
    if SessionManager.is_authenticated():
        st.success(f"Already logged in as {SessionManager.get_user().username}")
        if st.button("Logout"):
            SessionManager.logout()
            st.rerun()
    else:
        show_login_form()



if __name__ == "__main__":
    main()
