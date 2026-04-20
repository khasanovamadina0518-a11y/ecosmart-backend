# Railway Deploy Guide — EcoSmart Waste API

## 1. Railway Account yaratish

1. [Railway.app](https://railway.app) ga o'ting
2. GitHub akkaunt bilan ro'yxatdan o'ting
3. Yangi loyiha yarating

## 2. PostgreSQL Database qo'shish

1. Railway dashboard da "New" → "Database" → "PostgreSQL"
2. Database yaratilgandan keyin "Variables" tab dan `DATABASE_URL` ni ko'ring
3. Format: `postgresql://user:password@host:port/dbname`

## 3. Environment Variables sozlash

Railway loyihasida "Variables" tab ga o'ting va quyidagilarni qo'shing:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-super-secret-key-here-generate-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
APP_NAME=EcoSmart Waste
DEBUG=False
PORT=8000
```

**SECRET_KEY yaratish:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 4. GitHub Repository ulash

### Variant A: GitHub orqali deploy

1. Loyihangizni GitHub ga push qiling:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/ecosmart-api.git
git push -u origin main
```

2. Railway da "New" → "GitHub Repo" → Repositoriyangizni tanlang
3. Railway avtomatik deploy qiladi

### Variant B: Railway CLI orqali deploy

1. Railway CLI o'rnating:
```bash
npm i -g @railway/cli
```

2. Login qiling:
```bash
railway login
```

3. Loyihani link qiling:
```bash
railway link
```

4. Deploy qiling:
```bash
railway up
```

## 5. Deploy tekshirish

1. Railway dashboard da "Deployments" tab ni oching
2. Build logs ni kuzating
3. Deploy muvaffaqiyatli bo'lgandan keyin "Settings" → "Generate Domain"
4. Domain yaratiladi: `https://your-app.up.railway.app`

## 6. API test qilish

### Health Check
```bash
curl https://your-app.up.railway.app/
```

### API Documentation
```
https://your-app.up.railway.app/docs
```

### Register
```bash
curl -X POST "https://your-app.up.railway.app/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "phone": "+998901234567",
    "password": "test123",
    "city": "Tashkent"
  }'
```

## 7. Database Migration (agar kerak bo'lsa)

Railway da "PostgreSQL" service ni oching va "Connect" tugmasini bosing:

```bash
# Local dan Railway database ga ulanish
psql $DATABASE_URL

# Yoki Railway CLI orqali
railway run psql $DATABASE_URL
```

## 8. Logs ko'rish

```bash
railway logs
```

Yoki Railway dashboard da "Deployments" → "View Logs"

## 9. Troubleshooting

### Build xatosi
- `requirements.txt` faylini tekshiring
- Dockerfile sintaksisini tekshiring
- Railway logs ni o'qing

### Database connection xatosi
- `DATABASE_URL` to'g'ri formatda ekanligini tekshiring
- PostgreSQL service ishlab turganligini tekshiring
- `asyncpg` kutubxonasi o'rnatilganligini tekshiring

### Port xatosi
- Railway avtomatik `PORT` environment variable beradi
- Dockerfile da `$PORT` ishlatilganligini tekshiring

## 10. Production Best Practices

1. **DEBUG=False** qiling production da
2. **SECRET_KEY** ni random string bilan almashtiring
3. **CORS** da aniq domenlar ko'rsating (`allow_origins=["*"]` o'rniga)
4. **Database backup** sozlang
5. **Monitoring** qo'shing (Railway Metrics)

## 11. Custom Domain (optional)

1. Railway dashboard da "Settings" → "Domains"
2. "Custom Domain" qo'shing
3. DNS sozlamalarini yangilang

## 12. Scaling

Railway da avtomatik scaling mavjud:
- "Settings" → "Resources" → RAM va CPU sozlash

## Qo'shimcha Resurslar

- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL on Railway](https://docs.railway.app/databases/postgresql)
