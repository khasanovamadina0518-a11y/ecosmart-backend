from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    points = Column(Integer, default=0)
    eco_level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Hozircha bularni yopiq qoldiramiz
    # rewards = relationship("RewardClaim", back_populates="user")