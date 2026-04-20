from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class WasteTransaction(Base):
    __tablename__ = "waste_transactions"

    id = Column(Integer, primary_key=True, index=True)
    bin_id = Column(Integer, ForeignKey("bins.id"))
    amount = Column(Integer)  # Masalan, chiqindi miqdori

    # Relationship: Har bir tranzaksiya aniq bir bin (quti)ga tegishli
    # bin = relationship("Bin", back_populates="transactions")