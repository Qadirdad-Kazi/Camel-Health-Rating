import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from motor.motor_asyncio import AsyncIOMotorDatabase
import aiofiles
from typing import Optional

from app.database import get_database
from app.models.user import User
from app.models.camel import ImageRecord, ImageResponse, CamelRating
from app.services.auth_service import get_current_user
from app.services.ml_service import CamelMLService

# Create ML service instance
ml_service = CamelMLService()

# In-memory storage for demo purposes (replace with database in production)
prediction_storage = {}

router = APIRouter()

# Configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file"""
    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE} bytes"
        )
    
    # Check file extension
    if file.filename:
        file_ext = os.path.splitext(file.filename.lower())[1]
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

async def save_uploaded_file(file: UploadFile) -> tuple[str, str]:
    """Save uploaded file and return file path and filename"""
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return file_path, unique_filename

@router.post("/predict")
async def predict_camel_rating(
    file: UploadFile = File(...),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Upload camel image and get AI rating prediction"""
    try:
        # Validate file
        await validate_image_file(file)
        
        # Read file content for ML processing
        file_content = await file.read()
        
        # Log file details for debugging
        print(f"Processing file: {file.filename}, size: {len(file_content)} bytes")
        
        try:
            # Get ML prediction
            prediction = ml_service.predict(file_content)
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during prediction: {str(e)}"
            )
        
        # Save the uploaded file for reference
        file_ext = os.path.splitext(file.filename.lower())[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Generate unique ID for this prediction
        prediction_id = str(uuid.uuid4())
        
        # Store the prediction results
        prediction_storage[prediction_id] = {
            "id": prediction_id,
            "user_id": str(current_user.id) if current_user else None,
            "image_url": f"/uploads/{unique_filename}",
            "filename": unique_filename,
            "rating": prediction["rating"],
            "features": prediction["features"],
            "model": prediction.get("model", "unknown"),
            "confidence": prediction.get("confidence", 0.5),
            "model_info": prediction.get("model_info", {}),
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Generate response
        return prediction_storage[prediction_id]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )

@router.post("/predict-anonymous")
async def predict_camel_rating_anonymous(
    file: UploadFile = File(...)
):
    """Upload camel image and get AI rating prediction (anonymous)"""
    try:
        # Validate file
        await validate_image_file(file)
        
        # Read file content for ML processing
        file_content = await file.read()
        
        # Log file details for debugging
        print(f"Processing anonymous file: {file.filename}, size: {len(file_content)} bytes")
        
        try:
            # Get ML prediction
            prediction = ml_service.predict(file_content)
        except Exception as e:
            print(f"Anonymous prediction error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during prediction: {str(e)}"
            )
        
        # Save the uploaded file for reference
        file_ext = os.path.splitext(file.filename.lower())[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Generate unique ID for this prediction
        prediction_id = str(uuid.uuid4())
        
        # Store the prediction results
        prediction_storage[prediction_id] = {
            "id": prediction_id,
            "user_id": None,
            "image_url": f"/uploads/{unique_filename}",
            "filename": unique_filename,
            "rating": prediction["rating"],
            "features": prediction["features"],
            "model": prediction.get("model", "unknown"),
            "confidence": prediction.get("confidence", 0.5),
            "model_info": prediction.get("model_info", {}),
            "health_screening": prediction.get("health_screening", {}),
            "error": prediction.get("error", None),
            "message": prediction.get("message", None),
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Generate response
        return prediction_storage[prediction_id]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )

@router.get("/image/{image_id}")
async def get_image_details(image_id: str):
    """Get image details by ID from stored predictions"""
    try:
        # Check if we have stored prediction data for this image
        if image_id in prediction_storage:
            return prediction_storage[image_id]
        
        # If not found, return a not found error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving image"
        )
