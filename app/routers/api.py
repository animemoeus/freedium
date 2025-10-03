from fastapi import APIRouter, HTTPException
from app.services.url_service import URLService

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