import os
from dotenv import load_dotenv

# .env faylini yuklaymiz
load_dotenv()

db_url = os.getenv("DATABASE_URL")

if db_url:
    print("✅ MUVAFFAQIYAT: .env fayli topildi va o'qildi!")
    print(f"URL boshlanishi: {db_url[:20]}...") 
else:
    print("❌ XATO: .env fayli topilmadi yoki DATABASE_URL o'zgaruvchisi yo'q!")
    print(f"Hozirgi papka: {os.getcwd()}")