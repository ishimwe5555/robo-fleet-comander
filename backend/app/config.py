import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./robofleet.db")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

settings = Settings() 