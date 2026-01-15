import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)

    # Direct Neon connection string
    NEON_CONNECTION_STRING = os.environ.get("NEON_CONNECTION_STRING")
    
    if NEON_CONNECTION_STRING:
        SQLALCHEMY_DATABASE_URI = NEON_CONNECTION_STRING
    else:
        DB_USER = os.environ.get("DB_USER", "your_pg_user")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "your_pg_password")
        DB_HOST = os.environ.get("DB_HOST", "localhost")
        DB_PORT = os.environ.get("DB_PORT", "5432")
        DB_NAME = os.environ.get("DB_NAME", "matbakhna_db")
        DB_SSLMODE = os.environ.get("DB_SSLMODE", "require")

        SQLALCHEMY_DATABASE_URI = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


