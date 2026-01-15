## The Kitchen

مشروع Flask + PostgreSQL بواجهة HTML/CSS/JS (عربي/إنجليزي).

### التشغيل

1) تثبيت المتطلبات:

```bash
pip install -r requirements.txt
```

2) إنشاء ملف البيئة:

```bash
cp .env.example .env
```

3) ضبط متغيرات البيئة في ملف `.env`:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=matbakhna_db
SECRET_KEY=your-very-secure-secret-key-here
```

4) إنشاء الجداول:

```bash
flask --app app:create_app init-db
```

5) (اختياري) إضافة بيانات تجريبية:

```bash
flask --app app:create_app seed-db
```

6) تشغيل السيرفر:

```bash
python app.py
```

ثم افتح: `http://127.0.0.1:5000/`

### API Endpoints

#### Authentication
- `POST /api/auth/register` - تسجيل مستخدم جديد
- `POST /api/auth/login` - تسجيل الدخول
- `POST /api/auth/logout` - تسجيل الخروج
- `GET /api/auth/me` - جلب بيانات المستخدم الحالي

#### Products (CRUD)
- `GET /api/products` - جلب كل المنتجات
- `GET /api/products/<id>` - جلب منتج محدد
- `POST /api/products` - إضافة منتج (يحتاج admin)
- `PUT /api/products/<id>` - تعديل منتج (يحتاج admin)
- `DELETE /api/products/<id>` - حذف منتج (يحتاج admin)

### Security Updates Applied
- Added secure SECRET_KEY generation
- Added authentication and authorization
- Added CORS support
- Added input validation
- Added password hashing
- Environment-based configuration





