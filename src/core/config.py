from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv('MONGODB_URI')
    MONGODB_DATABASE: str = os.getenv("DB_NAME")
    PROJECT_NAME: str = "JobFusion CAP"
    VERSION: str = "1.0.0"

    PORT: int = os.getenv("PORT", 8001)  # Default to 8001 if not provided
    HOST: str = os.getenv("HOST", "0.0.0.0")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 43200))
    ALLOWED_HOSTS: list = ["*", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        extra = "allow" 

settings = Settings()