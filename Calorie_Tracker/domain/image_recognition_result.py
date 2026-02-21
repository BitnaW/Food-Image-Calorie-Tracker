"""Image recognition result domain model."""
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class FoodItemDetection:
    """Represents a detected food item in an image."""
    
    food_name: str
    confidence: float  # 0-1, confidence level
    food_type: str = None  # Generic category (e.g., "vegetable", "protein")


@dataclass
class ImageRecognitionResult:
    """Result from image recognition processing."""
    
    success: bool
    method: str  # "label_recognition" or "visual_estimation"
    detected_items: List[FoodItemDetection] = None
    extracted_calories: Optional[float] = None
    estimated_calories: Optional[float] = None
    confidence_score: Optional[float] = None
    error_message: Optional[str] = None
    raw_data: Optional[dict] = None  # Store any additional raw data
    
    def __post_init__(self):
        if self.detected_items is None:
            self.detected_items = []
