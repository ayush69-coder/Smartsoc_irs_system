"""
Logging configuration for PhishGuard Pro
"""

import logging
import sys
from loguru import logger
from app.core.config import settings

def setup_logging():
    """Setup structured logging"""
    
    # Remove default handler
    logger.remove()
    
    # Add console handler with structured logging
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level=settings.LOG_LEVEL,
        serialize=settings.LOG_FORMAT == "json"
    )
    
    # Add file handler for production
    if settings.ENVIRONMENT == "production":
        logger.add(
            "logs/phishguard.log",
            rotation="1 day",
            retention="30 days",
            level=settings.LOG_LEVEL,
            serialize=settings.LOG_FORMAT == "json"
        )
    
    # Configure standard library logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    return logger