"""Session management utilities."""
import streamlit as st
from typing import Optional
from ..domain import User


class SessionManager:
    """Manages user sessions via Streamlit session state."""
    
    SESSION_USER_KEY = "current_user"
    SESSION_AUTHENTICATED_KEY = "authenticated"
    
    @staticmethod
    def set_user(user: User):
        """Set current logged-in user."""
        st.session_state[SessionManager.SESSION_USER_KEY] = user
        st.session_state[SessionManager.SESSION_AUTHENTICATED_KEY] = True
    
    @staticmethod
    def get_user() -> Optional[User]:
        """Get current logged-in user."""
        return st.session_state.get(SessionManager.SESSION_USER_KEY)
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated."""
        return st.session_state.get(SessionManager.SESSION_AUTHENTICATED_KEY, False)
    
    @staticmethod
    def logout():
        """Clear user session."""
        if SessionManager.SESSION_USER_KEY in st.session_state:
            del st.session_state[SessionManager.SESSION_USER_KEY]
        if SessionManager.SESSION_AUTHENTICATED_KEY in st.session_state:
            del st.session_state[SessionManager.SESSION_AUTHENTICATED_KEY]
    
    @staticmethod
    def require_authentication():
        """Decorator to require user to be authenticated."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not SessionManager.is_authenticated():
                    st.error("Please log in first.")
                    st.stop()
                return func(*args, **kwargs)
            return wrapper
        return decorator
