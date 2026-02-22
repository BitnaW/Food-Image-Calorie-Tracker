"""Image recognition result domain model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class FoodItemDetection:
    """Represents a detected food item in an image."""

    calories: float
    food_name: str
    quantity: float
    unit: str
    # optional fields 
    source: Optional[str] = None
    food_type: Optional[str] = None
    notes: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class ImageRecognitionResult:
    """Result from image recognition processing."""
    
    success: bool
    method: str  # "label_recognition" or "visual_estimation"
    detected_items: List[FoodItemDetection] 
    extracted_calories: Optional[float] = None
    estimated_calories: Optional[float] = None
    confidence_score: Optional[float] = None
    error_message: Optional[str] = None
    raw_data: Optional[dict] = None  # Store any additional raw data
    
    def __post_init__(self):
        if self.detected_items is None:
            self.detected_items = []

    def convert_calorie_entires(self, user_id: int) -> list:
        entries = []
        for item in self.detected_items:
            entries.append(
                {
                    "user_id": user_id,
                    "calories": item.calories,
                    "food_name": item.food_name,
                    "food_type": item.food_type,
                    "quantity": item.quantity,
                    "unit": item.unit,
                    "source": "estimate",
                    "notes": item.notes,
                    "logged_at": datetime.now()
                }
            )
        return entries

