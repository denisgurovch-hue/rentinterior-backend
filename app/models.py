from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db import Base

# Enums для типов
class RoomType(str, enum.Enum):
    BEDROOM = "bedroom"
    LIVING_ROOM = "living_room"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"

class StyleType(str, enum.Enum):
    MINIMALIST = "minimalist"
    SCANDINAVIAN = "scandinavian"
    MODERN = "modern"
    CLASSIC = "classic"

class ProjectStatus(str, enum.Enum):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FurnitureCategory(str, enum.Enum):
    SOFA = "sofa"
    BED = "bed"
    TABLE = "table"
    CHAIR = "chair"
    WARDROBE = "wardrobe"
    SHELVING = "shelving"
    DECOR = "decor"
    LIGHTING = "lighting"

# Модели БД
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=True)  # Опционально для MVP
    room_type = Column(SQLEnum(RoomType), nullable=False)
    style = Column(SQLEnum(StyleType), nullable=False)
    budget = Column(Integer, nullable=False)  # В рублях
    city = Column(String, nullable=False)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.CREATED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    furniture_items = relationship("FurnitureItem", back_populates="project")

class FurnitureItem(Base):
    __tablename__ = "furniture_items"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    category = Column(SQLEnum(FurnitureCategory), nullable=False)
    price = Column(Integer, nullable=False)  # В рублях
    shop = Column(String, nullable=False)
    link = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    
    # Relationship
    project = relationship("Project", back_populates="furniture_items")
