from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List


# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# StagingTask Schemas
class StagingTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    is_completed: Optional[bool] = False


class StagingTaskCreate(StagingTaskBase):
    project_id: int


class StagingTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_completed: Optional[bool] = None


class StagingTask(StagingTaskBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Project with tasks
class ProjectWithTasks(Project):
    staging_tasks: List[StagingTask] = []

