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

def verify_user_credentials(username: str, password: str) -> bool:
    """Query database and verify user credentials."""
    db = get_database()
    
    # Query user by username
    result = db.fetch_one(
        "SELECT id, username, email, password_hash FROM users WHERE username = ?",
        (username,)
    )
    
    if not result:
        return False
    
    # Verify password
    stored_hash = result[3]  # password_hash is at index 3
    if not PasswordManager.verify_password(password, stored_hash):
        return False
    
    # Create user object and set session
    user = User(
        id=result[0],
        username=result[1],
        email=result[2],
        password_hash=stored_hash
    )
    SessionManager.set_user(user)
    return True


def show_login_form():
    st.title("CalorieCam")

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    #login mode
    if st.session_state.auth_mode == "login":
        st.subheader("Sign In")

        with st.form("login_form"):
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    # Query database and verify credentials
                    if verify_user_credentials(username, password):
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                        
        if st.button("Sign Up"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    
    if st.session_state.auth_mode == "signup":
        st.subheader("Create Account")
        

        new_username = st.text_input("New Username")
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        


        if st.button("Enter"):
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
                    valid, msg = AuthValidator.validate_password(new_password)
                    if not valid:
                        st.error(msg)
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        # Create user in database
                        try:
                            db = get_database()
                            password_hash = PasswordManager.hash_password(new_password)
                            
                            db.execute(
                                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                                (new_username, new_email, password_hash)
                            )

                            # Fetch the newly created user
                            result = db.fetch_one(
                                "SELECT id, username, email, password_hash FROM users WHERE username = ?",
                                (new_username,)
                            )
                            
                            if result:
                                # Log the user in automatically
                                user = User(
                                    id=result[0],
                                    username=result[1],
                                    email=result[2],
                                    password_hash=result[3]
                                )
                                SessionManager.set_user(user)
                                st.success(f"Welcome, {new_username}!")
                                st.rerun()
                        except Exception as e:
                            if "UNIQUE constraint failed" in str(e):
                                st.error("Username or email already exists")
                            else:
                                st.error(f"Error creating account: {str(e)}")

        if st.button("Return to Login"):
            st.session_state.auth_mode = "login"
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
