from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional

from app.database import get_database
from app.models.user import User
from app.models.camel import FeedbackCreate, Feedback, FeedbackResponse
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Submit feedback for a camel rating"""
    try:
        # Verify image exists
        image_data = await db.images.find_one({"_id": ObjectId(feedback_data.image_id)})
        if not image_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        # Check if user has already submitted feedback for this image
        existing_feedback = await db.feedback.find_one({
            "image_id": feedback_data.image_id,
            "user_id": str(current_user.id) if current_user else None
        })
        
        if existing_feedback:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback already submitted for this image"
            )
        
        # Create feedback record
        feedback_record = Feedback(
            user_id=str(current_user.id) if current_user else None,
            image_id=feedback_data.image_id,
            is_accurate=feedback_data.is_accurate,
            comment=feedback_data.comment
        )
        
        # Save to database
        result = await db.feedback.insert_one(feedback_record.dict())
        feedback_record.id = result.inserted_id
        
        return FeedbackResponse(
            id=str(feedback_record.id),
            user_id=feedback_record.user_id,
            image_id=feedback_record.image_id,
            is_accurate=feedback_record.is_accurate,
            comment=feedback_record.comment,
            created_at=feedback_record.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting feedback: {str(e)}"
        )

@router.get("/feedback/{image_id}", response_model=List[FeedbackResponse])
async def get_image_feedback(
    image_id: str,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all feedback for a specific image"""
    try:
        # Verify image exists
        image_data = await db.images.find_one({"_id": ObjectId(image_id)})
        if not image_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        # Get feedback for this image
        feedback_cursor = db.feedback.find({"image_id": image_id})
        feedback_list = []
        
        async for feedback_data in feedback_cursor:
            feedback_list.append(FeedbackResponse(
                id=str(feedback_data["_id"]),
                user_id=feedback_data.get("user_id"),
                image_id=feedback_data["image_id"],
                is_accurate=feedback_data["is_accurate"],
                comment=feedback_data.get("comment"),
                created_at=feedback_data["created_at"]
            ))
        
        return feedback_list
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving feedback"
        )

@router.get("/feedback-stats/{image_id}")
async def get_feedback_stats(
    image_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get feedback statistics for an image"""
    try:
        # Verify image exists
        image_data = await db.images.find_one({"_id": ObjectId(image_id)})
        if not image_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        # Get feedback statistics
        total_feedback = await db.feedback.count_documents({"image_id": image_id})
        accurate_feedback = await db.feedback.count_documents({
            "image_id": image_id,
            "is_accurate": True
        })
        inaccurate_feedback = await db.feedback.count_documents({
            "image_id": image_id,
            "is_accurate": False
        })
        
        accuracy_rate = (accurate_feedback / total_feedback * 100) if total_feedback > 0 else 0
        
        return {
            "image_id": image_id,
            "total_feedback": total_feedback,
            "accurate_feedback": accurate_feedback,
            "inaccurate_feedback": inaccurate_feedback,
            "accuracy_rate": round(accuracy_rate, 2)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving feedback statistics"
        )
