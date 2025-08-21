from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:Bharath08@localhost/parking_lot_management"
    
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    APP_NAME: str = "Parking Lot Management System"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    DEFAULT_PARKING_RATE_PER_HOUR: float = 5.0
    HANDICAP_PRIORITY_DISTANCE: int = 50
    LOT_FULL_THRESHOLD: float = 0.95
    
    class Config:
        env_file = ".env"


settings = Settings()