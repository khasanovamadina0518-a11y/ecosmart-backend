from app.core.database import Base
from .user import User
from .bin import Bin
from .waste import WasteTransaction
from .task import Task, UserTask
from .reward import Reward, RewardClaim

# Barcha modellarni bitta ro'yxatga yig'amiz
__all__ = ["Base", "User", "Bin", "WasteTransaction", "Task", "UserTask", "Reward", "RewardClaim"]