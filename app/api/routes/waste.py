from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional

from app.core.database import get_db
from app.models.bin import Bin 
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=None)
async def get_all_bins(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bazada mavjud barcha qutilarni ko'rish."""
    result = await db.execute(select(Bin))
    bins = result.scalars().all()
    return bins

@router.get("/{qr_code}", response_model=None)
async def get_bin_by_qr(
    qr_code: str, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """QR-kod orqali bitta qutini topish."""
    result = await db.execute(select(Bin).where(Bin.qr_code == qr_code))
    bin_item = result.scalars().first()

    if not bin_item:
        raise HTTPException(
            status_code=404, 
            detail=f"Kechirasiz, '{qr_code}' kodli quti topilmadi!"
        )
    return bin_item

@router.post("/submit")
async def submit_waste(
    qr_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Chiqindi topshirish va ball olish.
    """
    
    # 1. Qutini bazadan qidirish
    result = await db.execute(select(Bin).where(Bin.qr_code == qr_code))
    bin_item = result.scalars().first()
    
    if not bin_item:
        raise HTTPException(
            status_code=404, 
            detail="Noto'g'ri QR-kod! Bunday quti mavjud emas."
        )

    # 2. Ballarni hisoblash
    # earned_points o'zgaruvchisini aniqlaymiz
    earned_points = bin_item.points_per_use if bin_item.points_per_use else 10
    new_total_points = (current_user.points or 0) + earned_points
    
    # 3. Foydalanuvchi ballarini bazada yangilash
    await db.execute(
        update(User)
        .where(User.id == current_user.id)
        .values(points=new_total_points)
    )
    
    # 4. Saqlash
    await db.commit()
    
    # 5. Javob qaytarish (O'zgaruvchi nomlari to'g'irlandi)
    return {
        "status": "success",
        "message": "Chiqindi muvaffaqiyatli qabul qilindi",
        "points_earned": earned_points, # points emas, earned_points!
        "total_points": new_total_points, # user.points emas, yangi hisoblangan ball!
        "bin": bin_item.qr_code
    }