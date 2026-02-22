"""User information page."""
import streamlit as st
from datetime import datetime
from database import get_database
from domain import User
from utils import SessionManager, AuthValidator, PasswordManager


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
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.button("Update Profile"):
            try:
                db = get_database()
                updates_made = False
                
                # Validate and update email if changed
                if new_email != user.email:
                    valid, msg = AuthValidator.validate_email(new_email)
                    if not valid:
                        st.error(f"Email validation failed: {msg}")
                    else:
                        # Update email in database
                        db.execute(
                            "UPDATE users SET email = ? WHERE id = ?",
                            (new_email, user.id)
                        )
                        user.email = new_email
                        updates_made = True
                
                # Validate and update password if provided
                if new_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        valid, msg = AuthValidator.validate_password(new_password)
                        if not valid:
                            st.error(f"Password validation failed: {msg}")
                        else:
                            # Hash and update password in database
                            password_hash = PasswordManager.hash_password(new_password)
                            db.execute(
                                "UPDATE users SET password_hash = ? WHERE id = ?",
                                (password_hash, user.id)
                            )
                            user.password_hash = password_hash
                            updates_made = True
                
                if updates_made:
                    # Update session with new user info
                    SessionManager.set_user(user)
                    st.success("Profile updated successfully!")
                else:
                    st.info("No changes were made")
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    st.error("Email already in use by another account")
                else:
                    st.error(f"Error updating profile: {str(e)}")
        
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
