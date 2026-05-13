import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

print("\n=== Foydalanuvchilar ro'yxati ===")
cursor.execute('SELECT id, full_name, phone, created_at FROM users ORDER BY id DESC LIMIT 10')
users = cursor.fetchall()

if users:
    for row in users:
        print(f"ID: {row[0]}, Ism: {row[1]}, Tel: {row[2]}, Sana: {row[3]}")
else:
    print("Hech qanday foydalanuvchi topilmadi!")

print(f"\nJami foydalanuvchilar: {len(users)}")

conn.close()
