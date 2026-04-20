from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
# Bu yerda importlarni aniqlashtiramiz
from app.models.task import Task, UserTask, TaskStatus
from app.models.user import User  # Klass nomini aniq ko'rsatamiz

router = APIRouter()

@router.post("/start/{task_id}")
async def start_task(task_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # 1. Vazifa borligini tekshirish
        # scalars().first() ishlatish xavfsizroq va scalar_one_or_none dan ko'ra barqarorroq
        task_query = await db.execute(select(Task).where(Task.id == task_id))
        task = task_query.scalars().first()
        
        if not task:
            print(f"XATO: ID {task_id} bo'lgan vazifa topilmadi!")
            raise HTTPException(status_code=404, detail="Vazifa topilmadi")

        # 2. Foydalanuvchi borligini tekshirish
        user_query = await db.execute(select(User).where(User.id == user_id))
        user = user_query.scalars().first()
        
        if not user:
            print(f"XATO: ID {user_id} bo'lgan foydalanuvchi topilmadi!")
            raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

        # 3. Yangi vazifa yaratish
        new_user_task = UserTask(
            user_id=user_id,
            task_id=task_id,
            status=TaskStatus.PENDING.value # Enum bo'lsa .value ishlatish bazada xatolikni oldini oladi
        )
        
        db.add(new_user_task)
        await db.commit()
        # Refresh qilishdan oldin ob'ektni qayta yuklash (Async uchun muhim)
        await db.refresh(new_user_task)
        
        print(f"MUVAFFAQIYAT: Vazifa {user_id}-foydalanuvchi uchun saqlandi.")
        return new_user_task

    except Exception as e:
        # Xatoni terminalda to'liq ko'rish uchun:
        print("-" * 50)
        print(f"KRITIK XATO: {str(e)}")
        import traceback
        traceback.print_exc() # Bu xato qaysi qatorda ekanini ko'rsatadi
        print("-" * 50)
        # Sessionni tozalash (xato bo'lsa commit qilib bo'lmaydi)
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server xatosi: {str(e)}")