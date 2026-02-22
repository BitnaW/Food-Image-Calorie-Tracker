from fastapi import FastAPI, UploadFile, File, HTTPException
from google import genai
from dotenv import load_dotenv
import os
from backend.image_recognition import ImageProcessor

load_dotenv()

app = FastAPI()
client = genai.Client(api_key=os.getenv("GOOGLE_AI_API_KEY"))
processor = ImageProcessor()

@app.post("/estimate-calories")
async def estimate_calories(file: UploadFile = File(...)):
    image_bytes = await file.read()
    
    if not processor.validate_image(image_bytes):
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    result = processor.process_image(image_bytes, prefer_method="visual")
    return result