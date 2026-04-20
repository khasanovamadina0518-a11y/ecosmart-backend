"""
Security utilities — password hashing, JWT tokens, authentication
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db

# ── Password Hashing ──────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Parolni hash qilish (bcrypt)."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Parolni tekshirish."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT Token ─────────────────────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT access token yaratish."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # MUHIM: Xatolikni oldini olish uchun SECRET_KEY ni string ekanligiga ishonch hosil qilamiz
    # Agar settings.SECRET_KEY ichida '---BEGIN...' kabi yozuvlar bo'lsa, u PEM kutadi.
    # Biz HS256 ishlatganimiz uchun uni oddiy matn (string) sifatida uzatamiz.
    secret = str(settings.SECRET_KEY)
    
    # Algoritmni qat'iy HS256 qilib belgilaymiz (xatolikni kamaytirish uchun)
    encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")
    return encoded_jwt


# ── Authentication Dependency ─────────────────────
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Bearer token dan user_id olish va userni qaytarish."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token noto'g'ri yoki muddati o'tgan",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        secret = str(settings.SECRET_KEY)
        # Dekodlashda ham HS256 ishlatamiz
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        user_phone: str = payload.get("sub") # Biz tokenga phone raqamni sub qilib solganmiz
        
        if user_phone is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Import here to avoid circular dependency
    from app.models.user import User
    
    # Userni phone orqali bazadan qidiramiz (chunki token sub'ektida phone bor)
    result = await db.execute(select(User).where(User.phone == user_phone))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
    
    return user