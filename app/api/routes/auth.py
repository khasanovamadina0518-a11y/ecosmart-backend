from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(payload: UserLogin = Body(...), db: AsyncSession = Depends(get_db)):
    # Telefon raqamini normalize qilish (+ belgisini olib tashlash)
    phone = payload.phone.strip().replace('+', '').replace(' ', '').replace('-', '')
    print(f"🔐 Login urinishi: phone={phone} (original: {payload.phone})")
    
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalars().first()

    if not user:
        print(f"❌ Foydalanuvchi topilmadi: {phone}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Telefon yoki parol noto'g'ri.",
        )
    
    print(f"✅ Foydalanuvchi topildi: {user.full_name} (ID: {user.id})")
    print(f"🔑 Parolni tekshirish...")
    
    password_valid = verify_password(payload.password, user.hashed_password)
    print(f"🔑 Parol tekshiruvi natijasi: {password_valid}")
    
    if not password_valid:
        print(f"❌ Parol noto'g'ri!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Telefon yoki parol noto'g'ri.",
        )

    print(f"✅ Login muvaffaqiyatli: {user.full_name}")
    access_token = create_access_token(data={"sub": user.phone})
    return Token(access_token=access_token)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate = Body(...), db: AsyncSession = Depends(get_db)):
    # Telefon raqamini normalize qilish (+ belgisini olib tashlash)
    phone = payload.phone.strip().replace('+', '').replace(' ', '').replace('-', '')
    
    # Debug: Kelgan ma'lumotlarni ko'rsatish
    print(f"📥 Kelgan ma'lumotlar: full_name={payload.full_name}, phone={phone} (original: {payload.phone}), city={payload.city}, region={payload.region}")
    
    result = await db.execute(select(User).where(User.phone == phone))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu raqam allaqachon ro'yxatdan o'tgan.",
        )

    new_user = User(
        full_name=payload.full_name,
        phone=phone,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    print(f"✅ Yangi foydalanuvchi yaratildi: {new_user.id} - {new_user.full_name}")
    return {"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz."}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        phone=current_user.phone,
        username=None,
        email=None,
        city=None,
        eco_points=current_user.points or 0,
        eco_level=current_user.eco_level or 1,
        created_at=current_user.created_at,
    )
