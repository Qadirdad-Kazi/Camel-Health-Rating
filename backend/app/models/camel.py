from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler):
        return {"type": "string"}

class CamelFeatures(BaseModel):
    body_shape: str
    head_structure: str
    leg_condition: str
    coat_condition: str
    overall_fitness: str

class CamelRating(BaseModel):
    rating: int
    features: CamelFeatures

class ImageUpload(BaseModel):
    user_id: Optional[str] = None

class ImageRecord(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: Optional[str] = None
    image_url: str
    filename: str
    file_size: int
    rating: int
    features: CamelFeatures
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ImageResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    image_url: str
    filename: str
    rating: int
    features: CamelFeatures
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    image_id: str
    is_accurate: bool
    comment: Optional[str] = None

class Feedback(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: Optional[str] = None
    image_id: str
    is_accurate: bool
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class FeedbackResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    image_id: str
    is_accurate: bool
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
