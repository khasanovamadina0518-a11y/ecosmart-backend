from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

# 1. Sovg'alar jadvali
class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    points_required = Column(Integer, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Bog'liqlik: Ushbu sovg'aga tegishli barcha "da'volar" (claims)
    claims = relationship("RewardClaim", back_populates="reward")


# 2. Sotib olish tarixi jadvali
class RewardClaim(Base):
    __tablename__ = "reward_claims"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reward_id = Column(Integer, ForeignKey("rewards.id"), nullable=False)
    status = Column(String, default="claimed")
    
    # XATONI TUZATISH: created_at nomi claimed_at ga o'zgartirildi
    # Bu API route'dagi RewardClaim.claimed_at bilan moslikni ta'minlaydi
    claimed_at = Column(DateTime, default=datetime.utcnow) 

    # Relationship'lar
    user = relationship("User") 
    reward = relationship("Reward", back_populates="claims")