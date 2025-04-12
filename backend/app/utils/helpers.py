# app/utils/helpers.py
import logging
from fastapi import HTTPException
from typing import Any, Dict
from functools import wraps
import time

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(settings.LOG_FILE) if settings.LOG_FILE else logging.NullHandler()
        ]
    )

def handle_error(func):
    """Decorator to handle exceptions in routes"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
    return wrapper

def timer_decorator(func):
    """Decorator to measure execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def validate_language_code(lang_code: str) -> bool:
    """Validate if a language code is supported"""
    supported_languages = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'bn': 'Bengali'
    }
    return lang_code in supported_languages
