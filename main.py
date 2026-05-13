from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, Dict

app = FastAPI(title="EcoSmart Waste API")

# CORS sozlamalari - mobil uchun
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ MODELLAR ============
class UserRegister(BaseModel):
    full_name: str
    phone: str
    region: Optional[str] = None
    city: Optional[str] = None
    password: str
    
    class Config:
        extra = "allow"  # Har qanday qo'shimcha maydonni qabul qilish


class UserLogin(BaseModel):
    phone: str
    password: str


# ============ ENDPOINTLAR ============
@app.get("/")
def root():
    return {"message": "EcoSmart Waste API ishlayapti", "status": "active"}


@app.get("/api/health")
def health():
    return {"status": "ok", "server": "running"}


@app.post("/api/register")
def register(user: UserRegister):
    # region yoki city dan qaysi biri kelgan bo'lsa
    region_name = user.region if user.region else (user.city if user.city else "Noma'lum")
    
    print(f"📝 Ro'yxatdan o'tish: {user.full_name}, {user.phone}, {region_name}")
    
    return {
        "success": True,
        "message": f"Xush kelibsiz, {user.full_name}! Ro'yxatdan o'tish muvaffaqiyatli.",
        "user": {
            "full_name": user.full_name,
            "phone": user.phone,
            "region": region_name
        }
    }


@app.post("/api/login")
def login(login_data: UserLogin):
    print(f"🔐 Login: {login_data.phone}")
    
    return {
        "success": True,
        "message": "Tizimga kirish muvaffaqiyatli",
        "access_token": f"token_{login_data.phone}",
        "token_type": "bearer"
    }


@app.get("/api/me")
def get_me():
    return {
        "id": 1,
        "full_name": "Test User",
        "phone": "+998901234567",
        "region": "Toshkent"
    }


# Universal endpoint - har qanday ma'lumotni qabul qiladi
@app.post("/api/register/any")
async def register_any(request: Request):
    data = await request.json()
    print(f"📝 Qabul qilingan ma'lumot: {data}")
    
    return {
        "success": True,
        "message": "Ro'yxatdan o'tish muvaffaqiyatli",
        "received_data": data
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)