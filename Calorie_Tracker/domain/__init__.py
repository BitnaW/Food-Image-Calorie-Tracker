"""
Domain module containing shared data structures and models.
"""

from .user import User
from .calorie_entry import CalorieEntry
from .image_recognition_result import ImageRecognitionResult

__all__ = ["User", "CalorieEntry", "ImageRecognitionResult"]
