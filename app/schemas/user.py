from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserCreate(BaseModel):
    """Ro'yxatdan o'tish uchun schema."""
    full_name: str = Field(..., min_length=2, max_length=100, description="To'liq ism")
    phone: str = Field(..., description="Telefon raqam")
    password: str = Field(..., min_length=6, max_length=100, description="Parol")
    # Ixtiyoriy maydonlar:
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Foydalanuvchi nomi")
    email: Optional[EmailStr] = Field(None, description="Email")
    city: Optional[str] = Field(None, max_length=100, description="Shahar")

class UserLogin(BaseModel):
    """Login uchun schema."""
    phone: str = Field(..., description="Telefon raqam")
    password: str = Field(..., description="Parol")

class UserResponse(BaseModel):
    """User ma'lumotlarini qaytarish uchun schema."""
    id: int
    full_name: str
    phone: str
    username: Optional[str]
    email: Optional[str]
    city: Optional[str]
    eco_points: int = 0
    eco_level: int = 1
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """JWT token ichidagi ma'lumotlar."""
    user_id: Optional[int] = None