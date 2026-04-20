from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Bin(Base):
    __tablename__ = "bins"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String, unique=True, index=True)
    # Bazada bu ustun yo'qligi uchun xato beryapti, shuning uchun o'chirib turamiz:
    # name = Column(String) 
    bin_type = Column(String, nullable=True)
    points_per_use = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())