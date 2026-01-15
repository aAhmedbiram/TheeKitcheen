import os
from dotenv import load_dotenv

load_dotenv()


class SQLiteConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = "sqlite:///the_kitchen.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Use this config for testing while Neon is fixed
Config = SQLiteConfig
