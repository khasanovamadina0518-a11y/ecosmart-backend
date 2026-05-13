from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import auth, rewards, tasks, waste
from app.core.database import Base, engine
from app.models.bin import Bin
from app.models.reward import Reward, RewardClaim
from app.models.task import Task, UserTask
from app.models.user import User
from app.models.waste import WasteTransaction

app = FastAPI(
    title="EcoSmart Waste API",
    description="Ekologik chiqindilarni boshqarish va mukofotlash platformasi",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:19006",
        "http://127.0.0.1:19006",
        "*"  # Development uchun barcha originlarga ruxsat
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Validation xatolarini yaxshiroq ko'rsatish
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"❌ Validation xatosi: {exc}")
    print(f"📥 Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "message": "Ma'lumotlar validatsiyadan o'tmadi"
        },
    )


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()


app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(waste.router, prefix="/api/waste", tags=["Waste & Bins"])
app.include_router(rewards.router, prefix="/api/rewards", tags=["Rewards"])


@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "app": "EcoSmart Waste API",
        "version": "1.0.0",
        "message": "Server muvaffaqiyatli ishlayapti!",
    }


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
