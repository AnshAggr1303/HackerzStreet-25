# app/__init__.py
from fastapi import FastAPI
from app.config import settings  # Updated import path

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )
    return app