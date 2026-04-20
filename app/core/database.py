from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Ma'lumotlar bazasi manzili
DATABASE_URL = "postgresql+asyncpg://postgres:0m0ngfzY9C8OQb13@db.lgudiajvbuohwbfqmgty.supabase.co:5432/postgres"

# 1. Asinxron engine yaratish (Barqarorlik uchun qo'shimcha parametrlar bilan)
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,  # Ulanish uzilgan bo'lsa, avtomatik aniqlab qayta ulanadi
    pool_recycle=3600,   # Har soatda ulanishni yangilaydi (Supabase uzib qo'ymasligi uchun)
    pool_size=5,         # Bir vaqtning o'zida ochiq turadigan ulanishlar soni
    max_overflow=10      # Yuklama ortganda qo'shimcha ochiladigan ulanishlar
)

# 2. Asinxron sessiya yaratuvchisi
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. Modellar uchun asosiy Base klassi
Base = declarative_base()

# Bazaga ulanish funksiyasi (Dependency)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()