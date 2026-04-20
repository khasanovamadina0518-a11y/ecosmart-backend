"""
Rewards routes — mukofotlar bilan ishlash
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.reward import Reward, RewardClaim
from app.schemas.reward import RewardResponse, RewardClaimHistoryResponse, RewardClaimResponse

router = APIRouter()


@router.get("/", response_model=List[RewardResponse])
async def get_all_rewards(db: AsyncSession = Depends(get_db)):
    """
    Mavjud mukofotlar (is_active=True, stock>0, auth shart emas).
    """
    result = await db.execute(
        select(Reward)
        .where(Reward.is_active == True, Reward.stock > 0)
        .order_by(Reward.points_required)
    )
    rewards = result.scalars().all()
    
    return rewards


@router.get("/my", response_model=List[RewardClaimHistoryResponse])
async def get_my_rewards(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Joriy user ning mukofot tarixi (JWT talab qiladi).
    """
    result = await db.execute(
        select(RewardClaim)
        .options(selectinload(RewardClaim.reward))
        .where(RewardClaim.user_id == current_user.id)
        .order_by(RewardClaim.claimed_at.desc())
    )
    claims = result.scalars().all()
    
    return claims


@router.post("/{reward_id}/claim", response_model=RewardClaimResponse)
async def claim_reward(
    reward_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mukofot olish (JWT talab qiladi).
    """
    # 1. Reward mavjud va aktiv mi tekshirish
    result = await db.execute(select(Reward).where(Reward.id == reward_id))
    reward = result.scalar_one_or_none()
    
    if not reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mukofot topilmadi"
        )
    
    if not reward.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu mukofot aktiv emas"
        )
    
    # 2. Stock > 0 mi tekshirish
    if reward.stock <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sovg'a tugagan"
        )
    
    # 3. User da yetarli ball bormi tekshirish
    if current_user.points < reward.points_required:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Yetarli ball yo'q"
        )
    
    # 4. RewardClaim yaratish
    claim = RewardClaim(
        user_id=current_user.id,
        reward_id=reward_id,
        status="claimed"
    )
    db.add(claim)
    
    # 5. User dan ball ayirish
    current_user.points -= reward.points_required
    
    # 6. Stock kamaytirish
    reward.stock -= 1
    
    await db.commit()
    await db.refresh(current_user)
    
    return RewardClaimResponse(
        message="Mukofot muvaffaqiyatli olindi!",
        reward_title=reward.title,
        points_spent=reward.points_required,
        remaining_points=current_user.points
    )
