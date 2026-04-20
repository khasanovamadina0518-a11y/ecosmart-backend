"""
Waste schemas — Pydantic models for waste management
"""

from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class BinResponse(BaseModel):
    """Chiqindi qutisi ma'lumotlari."""
    id: int
    qr_code: str
    location_name: str
    bin_type: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class WasteSubmit(BaseModel):
    """Chiqindi topshirish uchun request schema."""
    qr_code: str = Field(..., description="Chiqindi qutisi QR kodi")
    waste_type: Literal["plastik", "qogoz", "shisha", "metall", "organik"] = Field(
        ..., description="Chiqindi turi"
    )
    weight: float = Field(..., gt=0, description="Chiqindi og'irligi (kg)")


class WasteSubmitResponse(BaseModel):
    """Chiqindi topshirish natijasi."""
    message: str
    points_earned: int
    new_total_points: int
    transaction_id: int
