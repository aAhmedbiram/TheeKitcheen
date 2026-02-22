import os
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

def _sanitize_db_url(db_url):
    """Sanitize database URL for logging (remove credentials)"""
    if not db_url:
        return "Not configured"
    
    try:
        parsed = urlparse(db_url)
        if parsed.scheme == 'postgresql':
            return f"{parsed.scheme}://[REDACTED]@{parsed.hostname}/{parsed.path.lstrip('/')}"
        else:
            return db_url
    except:
        return "Invalid URL format"

# Get project root for reliable .env loading
def _get_project_root():
    """Get project root directory"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'app.py').exists() and (current / 'config.py').exists():
            return current
        current = current.parent
    return Path.cwd()  # Fallback

# Load .env from project root (robust for Windows)
project_root = _get_project_root()
env_file = project_root / '.env'
load_dotenv(dotenv_path=env_file, override=False)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
    # Environment mode
    ENV = os.getenv("ENV", "development")
    
    # Database configuration logic
    raw_db_url = os.getenv("DATABASE_URL")
    
    if ENV == "production":
        # Production: REQUIRE DATABASE_URL
        if not raw_db_url:
            raise RuntimeError(
                "DATABASE_URL must be set in production mode. "
                "Set DATABASE_URL environment variable and restart the application."
            )
        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        # Development: DATABASE_URL is also required (no SQLite fallback)
        if not raw_db_url:
            raise RuntimeError(
                "DATABASE_URL must be set in all environments. "
                "Set DATABASE_URL environment variable to your Neon PostgreSQL connection string."
            )
        SQLALCHEMY_DATABASE_URI = raw_db_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Store sanitized version for logging
    SANITIZED_DB_URI = _sanitize_db_url(SQLALCHEMY_DATABASE_URI)
    
    # Set engine options based on database type
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
        # SQLite doesn't support pooling options
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": False,
            "connect_args": {"check_same_thread": False}
        }
    else:
        # PostgreSQL/MySQL engine options
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "pool_size": 10,
            "max_overflow": 20
        }
    
    # Delivery Configuration
    DELIVERY_HUBS = [
        {"lat": 30.1610413, "lng": 31.5609381},  # Future City hub
        {"lat": 30.0809753, "lng": 31.2355689}   # Shubra hub
    ]
    DELIVERY_NEAR_FEE = 50
    DELIVERY_FAR_FEE = 80
    DELIVERY_NEAR_KM = 25.0
    DELIVERY_MAX_KM = 70.0
    OSRM_BASE_URL = "https://router.project-osrm.org"
