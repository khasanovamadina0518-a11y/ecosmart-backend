"""
Test script to check authentication flow
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "="*50)
print("AUTHENTICATION TEST")
print("="*50)

# Test 1: Register yangi foydalanuvchi
print("\n1️⃣ Yangi foydalanuvchi yaratish...")
register_data = {
    "full_name": "Test User",
    "phone": "+998991234567",
    "password": "test123456"
}

try:
    response = requests.post(f"{BASE_URL}/api/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        print("✅ Ro'yxatdan o'tish muvaffaqiyatli!")
    elif response.status_code == 400:
        print("⚠️ Foydalanuvchi allaqachon mavjud")
    else:
        print(f"❌ Xatolik: {response.status_code}")
except Exception as e:
    print(f"❌ Xatolik: {e}")

# Test 2: Login
print("\n2️⃣ Login qilish...")
login_data = {
    "phone": "+998991234567",
    "password": "test123456"
}

try:
    response = requests.post(f"{BASE_URL}/api/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"✅ Login muvaffaqiyatli!")
        print(f"Token: {token[:50]}...")
    else:
        print(f"❌ Login xatosi: {response.status_code}")
except Exception as e:
    print(f"❌ Xatolik: {e}")

print("\n" + "="*50)
