from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.bin import Bin 
from app.core.security import get_current_user

router = APIRouter()

# 1. Barcha qutilarni olish
@router.get("/", response_model=None)
async def get_all_bins(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Bazada mavjud barcha qutilarni ko'rish."""
    result = await db.execute(select(Bin))
    bins = result.scalars().all()
    return bins

# 2. T-315: QR-kod orqali bitta qutini topish
@router.get("/{qr_code}", response_model=None)
async def get_bin_by_qr(
    qr_code: str, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    QR-kod orqali bitta qutini qidirish.
    Swagger-da TEST-001 deb yozib tekshirib ko'ring.
    """
    # Bazadan qr_code ustuni bo'yicha qidirish
    query = select(Bin).where(Bin.qr_code == qr_code)
    result = await db.execute(query)
    bin_item = result.scalars().first()

    # Agar bunday QR-kodli quti topilmasa
    if not bin_item:
        raise HTTPException(
            status_code=404, 
            detail=f"Kechirasiz, '{qr_code}' kodli quti tizimda mavjud emas!"
        )

    return bin_item