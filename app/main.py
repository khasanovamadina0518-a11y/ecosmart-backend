"""
EcoSmart Waste — Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, tasks, waste, rewards

# Import all models to ensure they are registered with Base
from app.models.user import User
from app.models.task import Task, UserTask
from app.models.bin import Bin
from app.models.waste import WasteTransaction
from app.models.reward import Reward, RewardClaim


# ── FastAPI App ───────────────────────────────────
app = FastAPI(
    title="EcoSmart Waste API",
    description="Ekologik chiqindilarni boshqarish va mukofotlash platformasi",
    version="1.0.0",
)


# ── CORS Middleware ───────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production da aniq domenlar ko'rsating
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Database Initialization ───────────────────────
@app.on_event("startup")
async def startup_event():
    """Server ishga tushganda database jadvallarini yaratish."""
    async with engine.begin() as conn:
        # Barcha jadvallarni yaratish (agar mavjud bo'lmasa)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database jadvallar tekshirildi va yaratildi")


@app.on_event("shutdown")
async def shutdown_event():
    """Server to'xtaganda database connection yopish."""
    await engine.dispose()
    print("🔌 Database connection yopildi")


# ── Routers ───────────────────────────────────────
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(waste.router, prefix="/waste", tags=["Waste & Bins"])
app.include_router(rewards.router, prefix="/rewards", tags=["Rewards"])


# ── Health Check ──────────────────────────────────
@app.get("/", tags=["Health"])
async def health_check():
    """API serverning ishlayotganini tekshirish."""
    return {
        "status": "ok",
        "app": "EcoSmart Waste API",
        "version": "1.0.0",
        "message": "Server muvaffaqiyatli ishlayapti!"
    }
