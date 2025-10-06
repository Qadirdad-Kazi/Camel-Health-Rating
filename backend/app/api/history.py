from fastapi import APIRouter, Depends, HTTPException, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_database
from app.models.user import User
from app.models.camel import ImageResponse
from app.services.auth_service import get_current_active_user

router = APIRouter()

@router.get("/history", response_model=List[ImageResponse])
async def get_user_history(
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    days: Optional[int] = Query(None, ge=1, le=365)
):
    """Get user's camel rating history"""
    try:
        # Build query
        query = {"user_id": str(current_user.id)}
        
        # Add date filter if specified
        if days:
            start_date = datetime.utcnow() - timedelta(days=days)
            query["created_at"] = {"$gte": start_date}
        
        # Get images with pagination
        cursor = db.images.find(query).sort("created_at", -1).skip(offset).limit(limit)
        
        images = []
        async for image_data in cursor:
            images.append(ImageResponse(
                id=str(image_data["_id"]),
                user_id=image_data.get("user_id"),
                image_url=image_data["image_url"],
                filename=image_data["filename"],
                rating=image_data["rating"],
                features=image_data["features"],
                created_at=image_data["created_at"]
            ))
        
        return images
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user history"
        )

@router.get("/history/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get user's rating statistics"""
    try:
        user_id = str(current_user.id)
        
        # Get total images
        total_images = await db.images.count_documents({"user_id": user_id})
        
        if total_images == 0:
            return {
                "total_images": 0,
                "average_rating": 0,
                "highest_rating": 0,
                "lowest_rating": 0,
                "rating_distribution": {}
            }
        
        # Get rating statistics
        pipeline = [
            {"$match": {"user_id": user_id}},
            {
                "$group": {
                    "_id": None,
                    "average_rating": {"$avg": "$rating"},
                    "highest_rating": {"$max": "$rating"},
                    "lowest_rating": {"$min": "$rating"},
                    "rating_counts": {
                        "$push": "$rating"
                    }
                }
            }
        ]
        
        result = await db.images.aggregate(pipeline).to_list(1)
        
        if result:
            stats = result[0]
            average_rating = round(stats["average_rating"], 2)
            
            # Calculate rating distribution
            rating_counts = {}
            for rating in stats["rating_counts"]:
                rating_counts[rating] = rating_counts.get(rating, 0) + 1
            
            return {
                "total_images": total_images,
                "average_rating": average_rating,
                "highest_rating": stats["highest_rating"],
                "lowest_rating": stats["lowest_rating"],
                "rating_distribution": rating_counts
            }
        else:
            return {
                "total_images": 0,
                "average_rating": 0,
                "highest_rating": 0,
                "lowest_rating": 0,
                "rating_distribution": {}
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user statistics"
        )

@router.delete("/history/{image_id}")
async def delete_user_image(
    image_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete a user's image and its associated data"""
    try:
        from bson import ObjectId
        
        # Verify image belongs to user
        image_data = await db.images.find_one({
            "_id": ObjectId(image_id),
            "user_id": str(current_user.id)
        })
        
        if not image_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found or access denied"
            )
        
        # Delete associated feedback
        await db.feedback.delete_many({"image_id": image_id})
        
        # Delete image record
        await db.images.delete_one({"_id": ObjectId(image_id)})
        
        # Delete physical file
        import os
        file_path = os.path.join("uploads", image_data["filename"])
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {"message": "Image deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting image"
        )
