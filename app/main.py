from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.routers import api, web
from app.services.redis_service import redis_service

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

    # Include routers
    app.include_router(api.router)
    app.include_router(web.router)

    # Event handlers
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        logger.info("Starting up application...")

        # Connect to Redis
        if redis_service.connect():
            logger.info("Redis connection established")
        else:
            logger.warning("Redis connection failed - continuing without Redis")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("Shutting down application...")
        redis_service.disconnect()

    return app

app = create_app()