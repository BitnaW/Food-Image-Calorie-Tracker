"""User domain model."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """Represents a user in the system."""
    
    id: int = None
    username: str = None
    email: str = None
    password_hash: str = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
