from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models import Project, FurnitureItem, ProjectStatus
from app.schemas import ProjectCreate, ProjectResponse, ProjectCreateResponse
from app.services.furniture import FurnitureService

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectCreateResponse, status_code=201)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """
    Создать новый проект меблировки
    """
    # 1. Создать проект в БД
    db_project = Project(
        room_type=project_data.room_type,
        style=project_data.style,
        budget=project_data.budget,
        city=project_data.city,
        status=ProjectStatus.PROCESSING
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    try:
        # 2. Подобрать мебель
        furniture_service = FurnitureService()
        selected_items = furniture_service.select_furniture(
            room_type=project_data.room_type.value,
            style=project_data.style.value,
            budget=project_data.budget
        )
        
        # 3. Сохранить предметы мебели
        total_cost = 0
        for item in selected_items:
            db_item = FurnitureItem(
                project_id=db_project.id,
                name=item["name"],
                category=item["category"],
                price=item["price"],
                shop=item["shop"],
                link=item["link"],
                image_url=item.get("image_url")
            )
            db.add(db_item)
            total_cost += item["price"]
        
        # 4. Обновить статус проекта
        db_project.status = ProjectStatus.COMPLETED
        db.commit()
        
        return ProjectCreateResponse(
            project_id=db_project.id,
            status=db_project.status,
            room_type=db_project.room_type,
            style=db_project.style,
            budget=db_project.budget,
            total_cost=total_cost,
            items_count=len(selected_items)
        )
        
    except Exception as e:
        db_project.status = ProjectStatus.FAILED
        db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Получить проект по ID
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Подсчитать общую стоимость
    total_cost = sum(item.price for item in project.furniture_items)
    
    response = ProjectResponse(
        id=project.id,
        room_type=project.room_type,
        style=project.style,
        budget=project.budget,
        city=project.city,
        status=project.status,
        created_at=project.created_at,
        furniture_items=project.furniture_items,
        total_cost=total_cost
    )
    
    return response

@router.get("/", response_model=List[ProjectResponse])
def list_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Список всех проектов (для будущего - фильтр по user_id)
    """
    projects = db.query(Project).offset(skip).limit(limit).all()
    
    result = []
    for project in projects:
        total_cost = sum(item.price for item in project.furniture_items)
        result.append(ProjectResponse(
            id=project.id,
            room_type=project.room_type,
            style=project.style,
            budget=project.budget,
            city=project.city,
            status=project.status,
            created_at=project.created_at,
            furniture_items=project.furniture_items,
            total_cost=total_cost
        ))
    
    return result

