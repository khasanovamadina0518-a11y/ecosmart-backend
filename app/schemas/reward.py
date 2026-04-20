"""
Reward schemas — Pydantic models for rewards management
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RewardResponse(BaseModel):
    """Mukofot ma'lumotlari."""
    id: int
    title: str
    description: Optional[str] = None
    points_required: int
    stock: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RewardClaimHistoryResponse(BaseModel):
    """Foydalanuvchi mukofot tarixi."""
    id: int
    reward_id: int
    status: str
    claimed_at: datetime
    reward: RewardResponse

    model_config = ConfigDict(from_attributes=True)


class RewardClaimResponse(BaseModel):
    """Mukofot olish natijasi."""
    message: str
    reward_title: str
    points_spent: int
    remaining_points: int


class RewardCreate(BaseModel):
    """Yangi mukofot yaratish uchun."""
    title: str
    description: Optional[str] = None
    points_required: int
    stock: int = 0