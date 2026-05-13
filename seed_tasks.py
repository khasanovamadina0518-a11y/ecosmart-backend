"""
Bazaga yangi tasklar qo'shish uchun skript
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.task import Task

async def seed_tasks():
    """Bazaga yangi tasklar qo'shish"""
    
    tasks_data = [
        {
            "title": "Plastik idishlarni ajrating",
            "description": "Uyingizdagi plastik idishlarni boshqa chiqindilardan ajrating va maxsus konteynerga tashlang.",
            "task_type": "recycling",
            "reward_points": 15,
            "is_completed": False,
        },
        {
            "title": "Qog'oz chiqindilarni yig'ing",
            "description": "Eski gazeta, jurnal va karton qutillarni yig'ib, qayta ishlash punktiga topshiring.",
            "task_type": "recycling",
            "reward_points": 20,
            "is_completed": False,
        },
        {
            "title": "Shisha idishlarni qaytaring",
            "description": "Bo'sh shisha idishlarni yig'ib, maxsus qabul punktlariga topshiring.",
            "task_type": "recycling",
            "reward_points": 25,
            "is_completed": False,
        },
        {
            "title": "Organik chiqindilarni kompostlang",
            "description": "Meva va sabzavot qoldiqlari, choy qoldiqlari va boshqa organik chiqindilarni kompost uchun ajrating.",
            "task_type": "composting",
            "reward_points": 30,
            "is_completed": False,
        },
        {
            "title": "Elektronika chiqindilarini topshiring",
            "description": "Eski telefon, kompyuter va boshqa elektronika qurilmalarini maxsus qabul punktlariga topshiring.",
            "task_type": "e-waste",
            "reward_points": 50,
            "is_completed": False,
        },
        {
            "title": "Batareyalarni to'g'ri utilizatsiya qiling",
            "description": "Ishlatilgan batareyalarni maxsus konteynerga tashlang, oddiy axlatga tashlamang.",
            "task_type": "hazardous",
            "reward_points": 20,
            "is_completed": False,
        },
        {
            "title": "Kiyim-kechak xayriyasiga topshiring",
            "description": "Eski lekin yaxshi holatdagi kiyimlaringizni xayriya tashkilotlariga topshiring.",
            "task_type": "donation",
            "reward_points": 15,
            "is_completed": False,
        },
        {
            "title": "Plastik qoplardan voz keching",
            "description": "Bir hafta davomida plastik qoplar o'rniga qayta foydalaniladigan sumkalardan foydalaning.",
            "task_type": "lifestyle",
            "reward_points": 25,
            "is_completed": False,
        },
        {
            "title": "Suv tejash bo'yicha amaliyot",
            "description": "Tish yuvish, idish yuvish va dush qabul qilishda suvni tejang.",
            "task_type": "conservation",
            "reward_points": 20,
            "is_completed": False,
        },
        {
            "title": "Ekologik mahsulotlar sotib oling",
            "description": "Kamida 3 ta ekologik toza mahsulot sotib oling (qayta ishlangan materialdan tayyorlangan).",
            "task_type": "shopping",
            "reward_points": 30,
            "is_completed": False,
        },
        {
            "title": "Daraxt eking",
            "description": "Mahallangizda yoki bog'ingizda kamida bitta daraxt eking.",
            "task_type": "planting",
            "reward_points": 100,
            "is_completed": False,
        },
        {
            "title": "Tozalash aksiyasida qatnashing",
            "description": "Mahalla yoki park tozalash aksiyasida ishtirok eting.",
            "task_type": "community",
            "reward_points": 40,
            "is_completed": False,
        },
    ]
    
    async with AsyncSessionLocal() as session:
        try:
            # Avval mavjud tasklar sonini tekshirish
            from sqlalchemy import select, func
            result = await session.execute(select(func.count(Task.id)))
            count = result.scalar()
            
            print(f"📊 Hozirda bazada {count} ta task mavjud")
            
            if count > 0:
                print("⚠️ Bazada allaqachon tasklar mavjud. Yangi tasklar qo'shilmoqda...")
            
            # Yangi tasklar qo'shish
            added_count = 0
            for task_data in tasks_data:
                # Bir xil nomli task borligini tekshirish
                result = await session.execute(
                    select(Task).where(Task.title == task_data["title"])
                )
                existing = result.scalars().first()
                
                if not existing:
                    task = Task(**task_data)
                    session.add(task)
                    added_count += 1
                    print(f"✅ Qo'shildi: {task_data['title']} ({task_data['reward_points']} ball)")
                else:
                    print(f"⏭️ Mavjud: {task_data['title']}")
            
            await session.commit()
            print(f"\n🎉 Jami {added_count} ta yangi task qo'shildi!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Xatolik: {e}")
            raise

if __name__ == "__main__":
    print("🌱 EcoSmart Waste - Tasklar qo'shish\n")
    asyncio.run(seed_tasks())
    print("\n✅ Tayyor!")
