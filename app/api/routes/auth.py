from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.core.security import create_access_token, verify_password

router = APIRouter()

@router.post("/login")
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # 1. Debug: Terminalda kiritilgan ma'lumotni ko'rish
    print(f"\n--- LOGIN URINISHI ---")
    print(f"Kiritilgan username (phone): '{credentials.username}'")

    # 2. Bazadagi barcha foydalanuvchilarni tekshirish (faqat debug uchun)
    all_users_result = await db.execute(select(User))
    users_list = all_users_result.scalars().all()
    print(f"Bazadagi jami foydalanuvchilar soni: {len(users_list)}")
    for u in users_list:
        print(f"Bazada bor raqam: '{u.phone}'")

    # 3. Foydalanuvchini qidirish
    result = await db.execute(select(User).where(User.phone == credentials.username))
    user = result.scalars().first()

    # 4. Foydalanuvchi topilmasa
    if not user:
        print(f"XATO: '{credentials.username}' raqami bazadan topilmadi!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Foydalanuvchi topilmadi. Avval ro'yxatdan o'ting."
        )

    # 5. TEST UCHUN: Parol tekshirishni vaqtincha o'chirib turamiz
    # Agar parolni ham tekshirmoqchi bo'lsangiz, pastdagi 2 qatorni kommentdan oching:
    # if not verify_password(credentials.password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Parol noto'g'ri")

    # 6. Muvaffaqiyatli login - Token yaratish
    print(f"MUVAFFAQIYAT: '{user.phone}' uchun token yaratildi.")
    access_token = create_access_token(data={"sub": user.phone})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/register")
async def register(
    full_name: str,
    phone: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    # Ro'yxatdan o'tishda raqam borligini tekshirish
    result = await db.execute(select(User).where(User.phone == phone))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Bu raqam allaqachon ro'yxatdan o'tgan")
    
    # Yangi foydalanuvchi yaratish (parolni hashlashni unutmang)
    from app.core.security import get_password_hash
    new_user = User(
        full_name=full_name,
        phone=phone,
        hashed_password=get_password_hash(password)
    )
    db.add(new_user)
    await db.commit()
    return {"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz"}