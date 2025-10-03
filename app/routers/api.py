from fastapi import APIRouter, HTTPException
from app.services.url_service import URLService
from app.services.redis_service import redis_service

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/")
def read_root():
    return {"message": "Hello World from API"}

@router.get("/validate-url")
def validate_url(url: str = ""):
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")

    if not URLService.is_valid_url(url):
        raise HTTPException(status_code=400, detail="URL is not valid")

    return {"url": url, "valid": True}

@router.get("/health")
def health_check():
    """Health check endpoint including Redis status"""
    redis_status = "connected" if redis_service.is_connected() else "disconnected"
    redis_ping = redis_service.ping() if redis_service.is_connected() else False

    return {
        "status": "healthy",
        "redis": {
            "status": redis_status,
            "ping": redis_ping
        }
    }

