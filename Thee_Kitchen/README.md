# 🍽️ Thee Kitchen Delivery System

A Flask-based food delivery system with real-time delivery quotes, order management, and multi-language support.

## 🚀 Quick Start (Windows)

### 1. Set up Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Create .env from example
Copy-Item .env.example .env

# Install dependencies
pip install -r requirements-dev.txt
```

### 2. Connect to Neon Database (Windows)

#### Neon PostgreSQL Setup:
```powershell
# Edit .env file and paste your Neon connection string
# Get connection string from Neon Console → Dashboard → Your Project

# Example .env content:
ENV=development
SECRET_KEY=change-me-in-production
DATABASE_URL=postgresql://USER:PASSWORD@HOST/neondb?sslmode=require

# Install PostgreSQL driver
pip install psycopg2-binary

# Start the application
python app.py
```

#### Production Setup:
```powershell
# Set production mode
$env:ENV="production"

# DATABASE_URL is REQUIRED in production
# Example production .env:
ENV=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://USER:PASSWORD@HOST/neondb?sslmode=require

# Start production app
python app.py
```

### 3. Verify Database Connection
```powershell
# Check which database the app is using
python -c "from config import Config; print(Config.SQLALCHEMY_DATABASE_URI)"

# Should show:
# For Neon: postgresql://USER:PASSWORD@HOST/neondb?sslmode=require

# Verify Neon connection directly
psql "$env:DATABASE_URL" -c "select current_database(), current_user, inet_server_addr();"
```

### 4. Run the Application
```powershell
# Start the development server
python app.py
```

The app will be available at `http://localhost:5000`

### 5. Run Tests
```powershell
# Run all tests
pytest -q -W error

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_delivery_quote.py -v
```

### Production Mode Setup
```powershell
# Set production mode
$env:ENV="production"

# DATABASE_URL is REQUIRED in production
# App will refuse to start without it

# Example production .env:
ENV=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://USER:PASSWORD@HOST/neondb?sslmode=require

# Start production app
python app.py
```

## ⚡ Neon Verification in 60 seconds

### Quick PowerShell Commands to Verify Neon Connection

```powershell
# 1) Ensure .env is in project root
dir .env

# Expected: .env file listed in directory

# 2) Show if dotenv sees DATABASE_URL
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('DATABASE_URL loaded:', bool(os.getenv('DATABASE_URL')))"

# Expected: DATABASE_URL loaded: True

# 3) Show what Config uses
python -c "from config import Config; print(Config.SQLALCHEMY_DATABASE_URI)"

# Expected: postgresql://USER:PASSWORD@HOST/neondb?sslmode=require

# 4) Run the verifier
python verify_db_connection.py

# Expected: ✅ Verification PASSED - Connected to Neon PostgreSQL

# 5) Start app and check startup banner
python app.py

# Expected: 
# 🚀 Thee Kitchen Starting Up
# 📊 ENV=development DB=postgresql://[REDACTED]@host/neondb
# 🔗 Connected DB: neondb user:your_user server:neon-server-ip
```

### If Verification Fails

**Issue: `.env` file not found**
```powershell
# Solution: Create .env from example
Copy-Item .env.example .env
# Edit .env with your Neon connection string
```

**Issue: DATABASE_URL not loaded**
```powershell
# Solution: Check .env file content
Get-Content .env | Select-String DATABASE_URL
# Ensure line: DATABASE_URL=postgresql://USER:PASSWORD@HOST/neondb?sslmode=require
```

**Issue: Connection string invalid**
```powershell
# Solution: Restart PowerShell and reload environment
# Close PowerShell, reopen, and run verification again
```

### Neon Credential Rotation (Security)

**If you exposed your connection string:**

1. **Go to Neon Console** → Dashboard → Your Project
2. **Navigate to Roles** → Select your database role
3. **Rotate Password** → Generate new secure password
4. **Update .env file** with new connection string
5. **Restart application** to use new credentials
6. **Verify connection** with `python verify_db_connection.py`

**Never share or commit .env files to version control!**

## 📋 Features

- 🛒 **Shopping Cart**: Add/remove items, real-time updates
- 🚚 **Delivery Quotes**: Real-time distance-based pricing via OSRM
- 👤 **User Authentication**: Secure login/registration system
- 🌍 **Multi-language**: Arabic & English support
- 📱 **Mobile Responsive**: Works on all devices
- 🔒 **Secure**: SQL injection protection, XSS prevention
- 📊 **Admin Dashboard**: Order management and analytics

## 🏗️ Project Structure

```
Thee_Kitchen/
├── app.py              # Main Flask application
├── config.py           # Configuration management
├── extensions.py       # SQLAlchemy extension
├── models.py           # Database models
├── delivery_service.py  # OSRM integration
├── translations.py     # Multi-language support
├── templates/          # Jinja2 templates
├── static/            # CSS, JS, images
├── tests/             # pytest test suite
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
└── .env.example       # Environment template
```

## 🧪 Testing

### Run Test Suite
```powershell
# All tests
pytest -q -W error

# With coverage
pytest --cov=. --cov-report=html

# Specific test categories
pytest tests/test_delivery_quote.py -v
pytest tests/test_checkout_and_order.py -v
```

### Test Categories
- **Unit Tests**: Model validation, business logic
- **Integration Tests**: API endpoints, database operations
- **Security Tests**: SQL injection, XSS, authentication
- **Performance Tests**: Query performance, concurrent users

## 🔧 Development

### Environment Setup
```powershell
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks (optional)
pre-commit install
```

### Code Quality
```powershell
# Format code
black .

# Lint code
flake8 .

# Security scan
bandit -r .
```

## 🗄️ Database Verification

### Ensure Correct Neon Database Connection

#### 1. Copy Connection String from Neon Console
1. Go to Neon Console → Dashboard → Your Project
2. Copy the connection string for the correct branch/database
3. **IMPORTANT**: Rotate password immediately if exposed

#### 2. Configure Environment
```powershell
# Create .env from example
Copy-Item .env.example .env

# Edit .env with your Neon connection string
# For production:
ENV=production
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DB?sslmode=require
SECRET_KEY=your-production-secret-key

# For development:
ENV=development
DATABASE_URL=sqlite:///thee_kitchen.db
```

#### 3. Verify Database Connection
```powershell
# Check what app uses
python -c "from config import Config; print(Config.SQLALCHEMY_DATABASE_URI)"

# Verify Neon connection directly
psql "$env:DATABASE_URL" -c "select current_database(), current_user, inet_server_addr();"

# Check app diagnostics (after login as admin)
curl -H "Cookie: session=your-admin-session" http://localhost:5000/admin/db-info
```

#### 4. Production Mode Safety
```powershell
# In production mode, DATABASE_URL is REQUIRED
# Set ENV=production to enable strict mode
# App will refuse to start without DATABASE_URL in production

# Test strict mode
$env:ENV="production"
python app.py  # Should fail without DATABASE_URL
```

### Database Diagnostics

#### Admin Database Info Endpoint
```powershell
# After logging in as admin, access:
GET /admin/db-info

# Returns safe database information:
{
  "status": "success",
  "database_info": {
    "database": "your_db_name",
    "user": "your_user",
    "server_ip": "neon-server-ip",
    "sqlalchemy_database_uri_sanitized": "postgresql://[REDACTED]@host/db"
  }
}
```

#### Startup Diagnostics
The app automatically logs database connection info at startup:
```
🔗 Connected DB: your_db_name user:your_user server:neon-server-ip
```

### Security Best Practices

#### Password Rotation
If DATABASE_URL was exposed:
1. Go to Neon Console
2. Rotate database role password
3. Update .env with new connection string
4. Restart application

#### Environment Isolation
- **Development**: Requires DATABASE_URL with Neon PostgreSQL connection
- **Production**: Requires DATABASE_URL with Neon PostgreSQL connection
- **Testing**: Uses test PostgreSQL database via conftest.py override

## 🗄️ Database

### Neon PostgreSQL (Required)
```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST/neondb?sslmode=require
```

### Database Migrations
```powershell
# Initialize database
python -c "
from extensions import db
from models import *
from app import app

with app.app_context():
    db.create_all()
    print('Database tables created')
"
```

## 🚀 Deployment

### Production Setup
1. Set environment variables:
   ```env
   FLASK_ENV=production
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=postgresql://user:password@host:5432/thekitchen
   ```

2. Install production dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Run with production server:
   ```powershell
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## 🔒 Security

- **SQL Injection Protection**: SQLAlchemy ORM prevents raw SQL
- **XSS Protection**: Input sanitization and template escaping
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Authentication**: Secure password hashing with bcrypt
- **HTTPS**: SSL certificates in production

## 🌍 Localization

### Adding New Languages
1. Add translations to `translations.py`
2. Update language switcher in templates
3. Test RTL/LTR layout as needed

### Supported Languages
- 🇸🇦 Arabic (Default, RTL)
- 🇬🇧 English (LTR)

## 📞 Troubleshooting

### Common Issues

#### Database Connection Error
```powershell
# Check .env file exists
Get-ChildItem .env

# Verify DATABASE_URL format
Get-Content .env | Select-String DATABASE_URL
```

#### Module Not Found
```powershell
# Install missing dependencies
pip install -r requirements-dev.txt

# Check virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Tests Fail
```powershell
# Clear cache
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force .pytest_cache

# Run with verbose output
pytest -v -s
```

### Health Check
```powershell
# Check application status
curl http://localhost:5000/health

# Check database connection
python -c "
from extensions import db
from app import app
with app.app_context():
    print('Database connected:', db.engine.url)
"
```

## 📊 Performance

### Optimization Tips
- Use database indexes for frequently queried columns
- Implement caching for delivery quotes
- Optimize image sizes in static files
- Enable gzip compression in production

### Benchmarks
- Database queries: <100ms for 1000 items
- API responses: <200ms
- Page loads: <500ms
- Concurrent users: 50+ supported

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the test files for usage examples
3. Check the GitHub issues page
4. Contact the development team

---

**Built with ❤️ using Flask, SQLAlchemy, and Neon PostgreSQL**
