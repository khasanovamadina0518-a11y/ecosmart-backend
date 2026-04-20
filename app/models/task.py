from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    task_type = Column(String, default="general")
    reward_points = Column(Integer, default=10)
    # is_active ustuni bazada yo'q bo'lsa, uni vaqtincha komment qiling:
    # is_active = Column(Boolean, default=True) 
    created_at = Column(DateTime, default=datetime.utcnow)

    # user_tasks = relationship("UserTask", back_populates="task")

class UserTask(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    status = Column(String, default="completed")
    completed_at = Column(DateTime, default=datetime.utcnow)

    # user = relationship("User", back_populates="user_tasks")
    # task = relationship("Task", back_populates="user_tasks")