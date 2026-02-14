import os
from dotenv import load_dotenv

load_dotenv()

def get_db_url() -> str:
    return os.getenv("DB_URL", "postgresql://postgres:Govind%40123@localhost:5432/maturity_db")

def get_upload_dir() -> str:
    return os.getenv("UPLOAD_DIR", "uploads")
