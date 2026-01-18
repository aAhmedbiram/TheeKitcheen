import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)

    # Check if we're in production (Fly.io)
    if os.environ.get("FLY_APP_NAME"):
        # Production: Use SQLite on persistent volume
        SQLALCHEMY_DATABASE_URI = "sqlite:////data/app.db"
    else:
        # Development: Use SQLite locally
        SQLALCHEMY_DATABASE_URI = "sqlite:///the_kitchen.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


