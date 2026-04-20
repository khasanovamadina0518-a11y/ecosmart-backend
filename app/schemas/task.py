"""
Task schemas — Pydantic models for task management
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TaskResponse(BaseModel):
    """Vazifa ma'lumotlari."""
    id: int
    title: str
    description: Optional[str] = None
    task_type: str
    reward_points: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TaskWithStatus(BaseModel):
    """Vazifa + joriy user uchun status."""
    id: int
    title: str
    description: Optional[str] = None
    task_type: str
    reward_points: int
    is_active: bool
    created_at: datetime
    user_status: Optional[str] = None  # "pending", "completed", yoki None
    
    model_config = ConfigDict(from_attributes=True)


class UserTaskResponse(BaseModel):
    """Foydalanuvchi vazifasi."""
    id: int
    task_id: int
    status: str
    completed_at: Optional[datetime] = None
    task: TaskResponse
    
    model_config = ConfigDict(from_attributes=True)


class TaskCompleteResponse(BaseModel):
    """Vazifa bajarilganda qaytadigan javob."""
    message: str
    points_earned: int
    new_total_points: int
    new_level: int


class TaskCreate(BaseModel):
    """Yangi vazifa yaratish uchun."""
    title: str
    description: Optional[str] = None
    task_type: str = "general"
    reward_points: int = 10