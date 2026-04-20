from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.core.database import get_db
from app.models.task import Task
from app.models.user import User  # User modelini bazaga yozish uchun chaqiramiz
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=None)
async def get_all_tasks(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Barcha vazifalarni olish."""
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks

@router.post("/{task_id}/complete")
async def complete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Vazifani yakunlash va foydalanuvchiga 10 ball berish (T-310 va T-311).
    """
    # 1. Vazifani bazadan qidirish
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID={task_id} bo'lgan vazifa topilmadi"
        )
    
    # 2. Agar vazifa allaqachon bajarilgan bo'lsa, ball qo'shmaymiz
    if task.is_completed:
        return {
            "status": "info",
            "message": "Bu vazifa avvalroq bajarilgan.",
            "current_points": current_user.points
        }

    try:
        # 3. Vazifa holatini yangilash
        task.is_completed = True
        
        # 4. Foydalanuvchi ballarini UPDATE qilish (Bazadagi 'points' ustuniga moslab)
        await db.execute(
            update(User)
            .where(User.id == current_user.id)
            .values(points=(User.points or 0) + 10)
        )

        # 5. O'zgarishlarni bazada saqlash (Commit)
        await db.commit()
        
        # 6. Foydalanuvchining yangi ballarini ko'rish uchun refresh qilamiz
        await db.refresh(current_user)
        
    except Exception as e:
        await db.rollback()
        print(f"BAZAGA YOZISHDA XATO: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Ballarni saqlashda xatolik yuz berdi"
        )

    return {
        "status": "success",
        "message": f"'{task.title}' vazifasi yakunlandi va sizga 10 ball berildi!",
        "new_total_points": current_user.points,
        "task_id": task.id
    }