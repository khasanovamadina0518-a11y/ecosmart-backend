# EcoSmart Waste — Setup Instructions

## 1. Virtual Environment yaratish va faollashtirish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

## 2. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

## 3. .env faylini sozlash

`.env.example` dan nusxa oling va o'z ma'lumotlaringizni kiriting:

```bash
cp .env.example .env
```

`.env` faylida quyidagilarni to'ldiring:
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — JWT uchun maxfiy kalit (random string)

## 4. Database jadvallarini yaratish

Python shell orqali:

```python
import asyncio
from app.core.database import create_tables

asyncio.run(create_tables())
```

Yoki alembic migration ishlatishingiz mumkin (tavsiya etiladi).

## 5. Serverni ishga tushirish

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 6. API Documentation

Server ishga tushgandan keyin:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 7. Test qilish

### Register (Ro'yxatdan o'tish)
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "phone": "+998901234567",
    "password": "test123",
    "city": "Tashkent"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+998901234567",
    "password": "test123"
  }'
```

### Get Current User (token bilan)
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Endpoints

- `POST /api/auth/register` — Yangi foydalanuvchi ro'yxatdan o'tkazish
- `POST /api/auth/login` — Login (JWT token olish)
- `GET /api/auth/me` — Joriy user ma'lumotlari (authentication kerak)
- `GET /` — Health check

## Yaratilgan fayllar

✅ `app/core/database.py` — Database connection va session management
✅ `app/core/security.py` — Password hashing va JWT authentication
✅ `app/models/user.py` — User SQLAlchemy modeli
✅ `app/schemas/user.py` — Pydantic schemas (validation)
✅ `app/api/routes/auth.py` — Authentication endpoints
✅ `app/main.py` — Auth router qo'shildi
✅ `requirements.txt` — asyncpg qo'shildi
