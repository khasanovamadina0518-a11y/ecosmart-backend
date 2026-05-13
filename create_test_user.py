import asyncio
import sqlite3
from app.core.security import get_password_hash

async def create_test_user():
    # SQLite connection
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Test foydalanuvchilar
    test_users = [
        {
            'full_name': 'Test User',
            'phone': '+998901234567',
            'password': 'test123'
        },
        {
            'full_name': 'Demo User',
            'phone': '+998881234567',
            'password': 'demo123'
        }
    ]
    
    for user in test_users:
        # Foydalanuvchi mavjudligini tekshirish
        cursor.execute('SELECT id FROM users WHERE phone = ?', (user['phone'],))
        existing = cursor.fetchone()
        
        if existing:
            print(f"✅ Foydalanuvchi allaqachon mavjud: {user['phone']}")
            continue
        
        # Parolni hash qilish
        hashed_password = get_password_hash(user['password'])
        
        # Yangi foydalanuvchi qo'shish
        cursor.execute('''
            INSERT INTO users (full_name, phone, hashed_password, points, eco_level, is_active, created_at)
            VALUES (?, ?, ?, 0, 1, 1, datetime('now'))
        ''', (user['full_name'], user['phone'], hashed_password))
        
        print(f"✅ Yangi foydalanuvchi yaratildi: {user['full_name']} - {user['phone']}")
    
    conn.commit()
    
    # Barcha foydalanuvchilarni ko'rsatish
    print("\n=== Barcha foydalanuvchilar ===")
    cursor.execute('SELECT id, full_name, phone FROM users')
    users = cursor.fetchall()
    for row in users:
        print(f"ID: {row[0]}, Ism: {row[1]}, Tel: {row[2]}")
    
    conn.close()

if __name__ == '__main__':
    asyncio.run(create_test_user())
