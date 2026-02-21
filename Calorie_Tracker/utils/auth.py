"""Authentication utilities."""
import hashlib
import secrets
from typing import Tuple


class PasswordManager:
    """Manages password hashing and verification."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password with salt."""
        salt = secrets.token_hex(16)
        pwdhash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${pwdhash.hex()}"
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        try:
            salt, pwdhash = password_hash.split('$')
            pwdhash_check = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return pwdhash_check.hex() == pwdhash
        except Exception:
            return False


class AuthValidator:
    """Validates authentication inputs."""
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate username format."""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 50:
            return False, "Username must be at most 50 characters"
        if not username.replace('_', '').replace('-', '').isalnum():
            return False, "Username can only contain letters, numbers, - and _"
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format."""
        if not email or '@' not in email:
            return False, "Invalid email format"
        if len(email) > 100:
            return False, "Email is too long"
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password strength."""
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters"
        if len(password) > 100:
            return False, "Password is too long"
        return True, ""
