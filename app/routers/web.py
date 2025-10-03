from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.services.url_service import URLService
from app.services.medium_service import MediumScraper

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Freedium - Home"}
    )

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request, "title": "About - Freedium"}
    )

@router.post("/validate", response_class=HTMLResponse)
async def validate_url_form(request: Request, url: str = Form(...)):
    is_valid = URLService.is_valid_url(url)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "title": "Validation Result - Freedium",
            "url": url,
            "is_valid": is_valid
        }
    )

@router.get("/medium", response_class=HTMLResponse)
async def medium_scraper(request: Request):
    return templates.TemplateResponse(
        "medium.html",
        {"request": request, "title": "Medium Scraper - Freedium"}
    )

@router.post("/medium", response_class=HTMLResponse)
async def scrape_medium_article(request: Request, url: str = Form(...)):
    if not url:
        return templates.TemplateResponse(
            "article.html",
            {
                "request": request,
                "title": "Error - Medium Scraper",
                "error": "URL is required",
                "article": {}
            }
        )

    scraper = MediumScraper()

    try:
        article_data = scraper.scrape_article(url)
        return templates.TemplateResponse(
            "article.html",
            {
                "request": request,
                "title": f"{article_data.get('title', 'Article')} - Freedium",
                "article": article_data,
                "error": None
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "article.html",
            {
                "request": request,
                "title": "Error - Medium Scraper",
                "error": str(e),
                "article": {}
            }
        )