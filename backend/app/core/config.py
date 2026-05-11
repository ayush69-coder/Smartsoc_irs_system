"""
Configuration settings for PhishGuard Pro
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    APP_NAME: str = "PhishGuard Pro"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "demo"
    DEBUG: bool = True
    
    # Server settings
    BACKEND_HOST: str = "localhost"
    BACKEND_PORT: int = 8000
    BACKEND_URL: str = "http://localhost:8000"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/phishguard.db"
    
    # JWT settings
    JWT_SECRET_KEY: str = "demo-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Model settings
    MODEL_PATH: str = "./data/models"
    MODEL_VERSION: str = "v1.0.0"
    
    # Sandbox settings
    SANDBOX_TIMEOUT: int = 30
    SANDBOX_MEMORY_LIMIT: int = 512
    
    # Playwright settings
    PLAYWRIGHT_BROWSER_PATH: str = "/usr/bin/chromium-browser"
    PLAYWRIGHT_HEADLESS: bool = True
    
    # Demo settings
    DEMO_DATA_PATH: str = "./data/demo_campaigns.json"
    DEMO_MODE: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Security
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Extension
    EXTENSION_ID: str = "phishguard-pro-extension"
    EXTENSION_VERSION: str = "1.0.0"
    
    # Compliance
    PII_MASKING: bool = True
    DATA_RETENTION_DAYS: int = 30
    TELEMETRY_ENABLED: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()