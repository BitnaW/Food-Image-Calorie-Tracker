"""Login page."""
import streamlit as st
from ..database import get_database, DatabaseSchema
from ..domain import User
from ..utils import SessionManager, PasswordManager, AuthValidator


def show_login_form():
    """Display login form."""
    st.title("Login")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", key="login_btn"):
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                # TODO: Query database and verify credentials
                st.info("Login functionality coming soon - database integration needed")
    
    with col2:
        st.subheader("Create Account")
        new_username = st.text_input("New Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up", key="signup_btn"):
            # Validate inputs
            valid, msg = AuthValidator.validate_username(new_username)
            if not valid:
                st.error(msg)
            else:
                valid, msg = AuthValidator.validate_email(new_email)
                if not valid:
                    st.error(msg)
                else:
                    valid, msg = AuthValidator.validate_password(new_password)
                    if not valid:
                        st.error(msg)
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        # TODO: Create user in database
                        st.info("Sign up functionality coming soon - database integration needed")


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
