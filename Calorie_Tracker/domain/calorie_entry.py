"""Calorie entry domain model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CalorieEntry:
    """Represents a calorie entry for a user."""
    
    id: int = None
    user_id: int = None
    calories: float = None
    food_name: str = None
    food_type: str = None  # e.g., "vegetable", "protein", "grain"
    quantity: float = None  # numeric amount
    unit: str = None  # e.g., "grams", "cups", "oz"
    source: str = None  # "label" or "estimate"
    image_path: Optional[str] = None  # Path to the image if provided
    notes: Optional[str] = None
    logged_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.logged_at is None:
            self.logged_at = datetime.now()
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
