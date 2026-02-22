"""Image recognition module for calorie extraction."""
from abc import ABC, abstractmethod
from PIL import Image
from domain import ImageRecognitionResult, FoodItemDetection
from google import genai
from google.genai import types
import os
import io
import json

# base method for the other types of img recognizers to inherit from
class ImageRecognizer(ABC):
    """Abstract base class for image recognition strategies."""
    
    @abstractmethod
    def recognize(self, image_bytes: bytes) -> ImageRecognitionResult:
        """Recognize food in image and return result."""
        pass


class LabelRecognizer(ImageRecognizer):
    """Recognizes nutritional labels in images."""

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_AI_API_KEY"))
            
    def recognize(self, image_bytes: bytes) -> ImageRecognitionResult:
        """
        Attempt to extract calorie information from a nutritional label.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            ImageRecognitionResult with extracted calories
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-3.1-pro-preview",
                contents=[
                    """Analyze this food label and respond in this exact JSON format, no other text:
                    {
                        "detected_items": [
                            {
                                "calories": 350,
                                "food_name": "Grilled Chicken Breast",
                                "food_type": "protein",
                                "quantity": 1,
                                "unit": "serving",
                                "source": "estimation",
                                "notes": "Approximately 200g, lightly seasoned"
                            }
                        ],
                        "estimated_calories": 500,
                        "confidence_score": 0.8
                    }""",
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                ])

            data = json.loads(response.text)
            
            result = ImageRecognitionResult(
                success=True,
                method="label_recognition",
                detected_items=[FoodItemDetection(**item) for item in data["detected_items"]],
                estimated_calories=data["estimated_calories"],
                confidence_score=data["confidence_score"]
            )
            return result
        
        except Exception as e:
            return ImageRecognitionResult(
                success=False,
                method="label_recognition",
                detected_items=[],
                error_message=str(e)
            )


class VisualEstimator(ImageRecognizer):
    """Estimates calories based on visual food detection and generic formulas."""
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_AI_API_KEY"))
            
    def recognize(self, image_bytes: bytes) -> ImageRecognitionResult:
        """
        Estimate calories based on detected food items.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            ImageRecognitionResult with estimated calories
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-3.1-pro-preview",
                contents=[
                    """Analyze this food image and respond in this exact JSON format, no other text:
                    {
                        "detected_items": [
                            {
                                "calories": 350,
                                "food_name": "Grilled Chicken Breast",
                                "food_type": "protein",
                                "quantity": 1,
                                "unit": "serving",
                                "source": "estimation",
                                "notes": "Approximately 200g, lightly seasoned"
                            }
                        ],
                        "estimated_calories": 500,
                        "confidence_score": 0.8
                    }""",
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                ])
            
            data = json.loads(response.text)

            result = ImageRecognitionResult(
                success=True,
                method="visual_estimation",
                detected_items=[FoodItemDetection(**item) for item in data["detected_items"]],
                estimated_calories=data["estimated_calories"],
                confidence_score=data["confidence_score"]
                )
            return result
        
        except Exception as e:
            return ImageRecognitionResult(
                success=False,
                method="visual_estimation",
                detected_items=[],
                error_message=str(e)
            )
            

class ImageProcessor:
    """Main processor for image-based calorie extraction."""
    
    def __init__(self):
        self.label_recognizer = LabelRecognizer()
        self.visual_estimator = VisualEstimator()
    
    def process_image(
        self,
        image_bytes: bytes,
        prefer_method: str = None
    ) -> ImageRecognitionResult:
        """
        Process image to extract or estimate calories.
        
        Args:
            image_bytes: Raw image bytes
            prefer_method: Preferred method ("label" or "visual"), tries preferred first
            
        Returns:
            ImageRecognitionResult
        """
        # Try preferred method first if specified
        if prefer_method == "label":
            result = self.label_recognizer.recognize(image_bytes)
            if result.success:
                return result
            # Fall back to visual estimation
            return self.visual_estimator.recognize(image_bytes)
        
        elif prefer_method == "visual":
            result = self.visual_estimator.recognize(image_bytes)
            if result.success:
                return result
            # Fall back to label recognition
            return self.label_recognizer.recognize(image_bytes)
        
        # Try both methods and return best result
        label_result = self.label_recognizer.recognize(image_bytes)
        visual_result = self.visual_estimator.recognize(image_bytes)
        
        # Prefer label recognition if successful
        if label_result.success:
            return label_result
        return visual_result
    
    def validate_image(self, image_bytes: bytes) -> bool:
        """Validate that bytes contain a valid image."""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
            return True
        except Exception:
            return False
