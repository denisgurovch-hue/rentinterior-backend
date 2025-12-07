from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models import RoomType, StyleType, ProjectStatus, FurnitureCategory

# Request schemas
class ProjectCreate(BaseModel):
    room_type: RoomType
    style: StyleType
    budget: int = Field(gt=0, description="Бюджет в рублях")
    city: str = Field(min_length=2, description="Город")

# Response schemas
class FurnitureItemResponse(BaseModel):
    id: int
    name: str
    category: FurnitureCategory
    price: int
    shop: str
    link: str
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: int
    room_type: RoomType
    style: StyleType
    budget: int
    city: str
    status: ProjectStatus
    created_at: datetime
    furniture_items: List[FurnitureItemResponse] = []
    total_cost: int = 0
    
    class Config:
        from_attributes = True

class ProjectCreateResponse(BaseModel):
    project_id: int
    status: ProjectStatus
    room_type: RoomType
    style: StyleType
    budget: int
    total_cost: int
    items_count: int
