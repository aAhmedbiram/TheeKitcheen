import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)
    
    # Session configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'
    
    # Check if we're in production (Fly.io)
    if os.environ.get("FLY_APP_NAME"):
        # Production: Use Neon database
        SQLALCHEMY_DATABASE_URI = "postgresql://neondb_owner:npg_6GExLcegj1ph@ep-holy-smoke-ahbl1aqc-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    else:
        # Development: Use SQLite
        SQLALCHEMY_DATABASE_URI = "sqlite:///the_kitchen.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


