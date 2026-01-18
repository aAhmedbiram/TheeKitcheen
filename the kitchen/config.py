import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)

    # Check if we're in production (Fly.io)
    if os.environ.get("FLY_APP_NAME"):
        # Production: Use Neon database
        NEON_CONNECTION_STRING = os.environ.get("NEON_CONNECTION_STRING")
        if NEON_CONNECTION_STRING:
            SQLALCHEMY_DATABASE_URI = NEON_CONNECTION_STRING
        else:
            DB_USER = os.environ.get("DB_USER")
            DB_PASSWORD = os.environ.get("DB_PASSWORD")
            DB_HOST = os.environ.get("DB_HOST")
            DB_PORT = os.environ.get("DB_PORT", "5432")
            DB_NAME = os.environ.get("DB_NAME")
            DB_SSLMODE = os.environ.get("DB_SSLMODE", "require")
            SQLALCHEMY_DATABASE_URI = (
                f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"
            )
    else:
        # Development: Use SQLite
        SQLALCHEMY_DATABASE_URI = "sqlite:///the_kitchen.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


