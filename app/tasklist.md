# ✅ EcoSmart Waste — To'liq Tasklist
> Har bir task mustaqil, mayda va bajarilishi oson qilib yozilgan.
> ☐ = bajarilmagan | ✅ = bajarilgan
> **AI agent ishlatish:** Har bir task uchun `prompts.md` dan tegishli promptni oling.
 
---
 
## 🗂️ MODUL 0 — TAYYORGARLIK (1-kun)
 
### 0.1 Hisob va asboblar
- ☐ **T-001** — [Supabase.com](https://supabase.com) da bepul hisob ochish
- ☐ **T-002** — Supabase da yangi project yaratish (nom: `ecosmart-waste`)
- ☐ **T-003** — Supabase → Settings → Database → Connection string ni nusxalash
- ☐ **T-004** — [Railway.app](https://railway.app) da GitHub bilan hisob ochish
- ☐ **T-005** — [GitHub.com](https://github.com) da yangi repo yaratish: `ecosmart-backend`
- ☐ **T-006** — [GitHub.com](https://github.com) da yangi repo yaratish: `ecosmart-mobile`
- ☐ **T-007** — Kompyuterga [VS Code](https://code.visualstudio.com) o'rnatish
- ☐ **T-008** — VS Code ga `Python` extension o'rnatish
- ☐ **T-009** — VS Code ga `React Native Tools` extension o'rnatish
- ☐ **T-010** — Telefoningizga `Expo Go` ilovasini o'rnatish (Play Store / App Store)
- ☐ **T-011** — [Node.js](https://nodejs.org) o'rnatish (LTS versiya)
- ☐ **T-012** — Python o'rnatish (3.11+)
### 0.2 Papka tuzilmasi
- ☐ **T-013** — Kompyuterda `ecosmart` nomli asosiy papka yaratish
- ☐ **T-014** — Ichida `backend` papkasi yaratish
- ☐ **T-015** — Ichida `mobile` papkasi yaratish
---
 
## 🗂️ MODUL 1 — BACKEND: ASOSIY STRUKTURA (2-kun)
 
### 1.1 Loyiha skelet
- ☐ **T-101** — `backend` papkasida `app` papkasi yaratish
- ☐ **T-102** — AI agent bilan **Prompt B-01** ishlatib papka strukturasini yaratish
- ☐ **T-103** — `requirements.txt` faylini yaratish (AI agent yozadi)
- ☐ **T-104** — Terminal da `pip install -r requirements.txt` buyrug'ini ishlatish
- ☐ **T-105** — `.env` fayl yaratish va Supabase connection string ni qo'shish
- ☐ **T-106** — `.gitignore` fayl yaratish (`.env` ni ignore qilishi kerak)
### 1.2 Database ulanish
- ☐ **T-107** — AI agent bilan **Prompt B-02** ishlatib `app/core/database.py` yozish
- ☐ **T-108** — `python -c "from app.core.database import engine; print('OK')"` buyrug'i ishlashini tekshirish
- ☐ **T-109** — Supabase dashboard da ulanish muvaffaqiyatli ekanini tekshirish
### 1.3 Asosiy config
- ☐ **T-110** — AI agent bilan **Prompt B-03** ishlatib `app/core/config.py` yozish
- ☐ **T-111** — AI agent bilan **Prompt B-04** ishlatib `app/core/security.py` (JWT) yozish
- ☐ **T-112** — `app/main.py` yaratish va FastAPI app ishga tushirish
- ☐ **T-113** — `uvicorn app.main:app --reload` buyrug'i ishlaganini tekshirish
- ☐ **T-114** — Brauzerda `http://localhost:8000/docs` ochilishini tekshirish ✨
---
 
## 🗂️ MODUL 2 — BACKEND: MODELLAR (2-3 kun)
 
### 2.1 User modeli
- ☐ **T-201** — AI agent bilan **Prompt B-05** ishlatib `app/models/user.py` yozish
- ☐ **T-202** — AI agent bilan **Prompt B-06** ishlatib `app/schemas/user.py` yozish
- ☐ **T-203** — Supabase da `users` jadval avtomatik yaratilganini tekshirish
### 2.2 Task modeli
- ☐ **T-204** — AI agent bilan **Prompt B-07** ishlatib `app/models/task.py` yozish
- ☐ **T-205** — AI agent bilan **Prompt B-08** ishlatib `app/schemas/task.py` yozish
- ☐ **T-206** — Supabase da `tasks` va `user_tasks` jadvallar yaratilganini tekshirish
### 2.3 Waste modeli
- ☐ **T-207** — AI agent bilan **Prompt B-09** ishlatib `app/models/waste.py` yozish
- ☐ **T-208** — AI agent bilan **Prompt B-10** ishlatib `app/schemas/waste.py` yozish
- ☐ **T-209** — Supabase da `bins` va `waste_transactions` jadvallar yaratilganini tekshirish
### 2.4 Reward modeli
- ☐ **T-210** — AI agent bilan **Prompt B-11** ishlatib `app/models/reward.py` yozish
- ☐ **T-211** — AI agent bilan **Prompt B-12** ishlatib `app/schemas/reward.py` yozish
- ☐ **T-212** — Supabase da `rewards` va `reward_claims` jadvallar yaratilganini tekshirish
---
 
## 🗂️ MODUL 3 — BACKEND: API ROUTELAR (3-4 kun)
 
### 3.1 Auth API
- ☐ **T-301** — AI agent bilan **Prompt B-13** ishlatib `app/api/routes/auth.py` yozish
- ☐ **T-302** — Swagger da `POST /auth/register` ni test qilish
- ☐ **T-303** — Swagger da `POST /auth/login` ni test qilish
- ☐ **T-304** — Swagger da `GET /auth/me` ni JWT token bilan test qilish
- ☐ **T-305** — Supabase da yangi user paydo bo'lganini tekshirish
### 3.2 Tasks API
- ☐ **T-306** — AI agent bilan **Prompt B-14** ishlatib `app/api/routes/tasks.py` yozish
- ☐ **T-307** — Supabase da qo'lda 3 ta test task qo'shish (SQL editor orqali)
- ☐ **T-308** — Swagger da `GET /tasks` ni test qilish
- ☐ **T-309** — Swagger da `GET /tasks/my` ni test qilish
- ☐ **T-310** — Swagger da `POST /tasks/{id}/complete` ni test qilish
- ☐ **T-311** — User points oshganini tekshirish (Supabase da)
### 3.3 Waste API
- ☐ **T-312** — AI agent bilan **Prompt B-15** ishlatib `app/api/routes/waste.py` yozish
- ☐ **T-313** — Supabase da qo'lda 2 ta test bin qo'shish (qr_code: "TEST-001", "TEST-002")
- ☐ **T-314** — Swagger da `GET /bins` ni test qilish
- ☐ **T-315** — Swagger da `GET /bins/{qr_code}` ni test qilish
- ☐ **T-316** — Swagger da `POST /waste/submit` ni test qilish
- ☐ **T-317** — Points hisoblanganini tekshirish
### 3.4 Rewards API
- ☐ **T-318** — AI agent bilan **Prompt B-16** ishlatib `app/api/routes/rewards.py` yozish
- ☐ **T-319** — Supabase da qo'lda 3 ta test reward qo'shish
- ☐ **T-320** — Swagger da `GET /rewards` ni test qilish
- ☐ **T-321** — Swagger da `POST /rewards/{id}/claim` ni test qilish
- ☐ **T-322** — Points ayirilganini tekshirish
- ☐ **T-323** — Yetarli points bo'lmaganda xato qaytarishini tekshirish
### 3.5 Router ulash
- ☐ **T-324** — AI agent bilan **Prompt B-17** ishlatib barcha routerlarni `main.py` ga ulash
- ☐ **T-325** — Swagger da barcha endpointlar ko'rinishini tekshirish
---
 
## 🗂️ MODUL 4 — BACKEND: DEPLOY (4-5 kun)
 
- ☐ **T-401** — AI agent bilan **Prompt B-18** ishlatib `Dockerfile` yozish
- ☐ **T-402** — GitHub ga barcha backend kodlarni push qilish
- ☐ **T-403** — Railway.app da "New Project" → "Deploy from GitHub" tanlash
- ☐ **T-404** — Railway da environment variables qo'shish (DATABASE_URL, SECRET_KEY)
- ☐ **T-405** — Deploy muvaffaqiyatli bo'lganini tekshirish
- ☐ **T-406** — Railway da berilgan URL ni nusxalash va eslab qolish
- ☐ **T-407** — Brauzerda `https://[railway-url]/docs` ochilishini tekshirish ✨
- ☐ **T-408** — Railway URL ni `mobile/services/api.ts` uchun saqlash
---