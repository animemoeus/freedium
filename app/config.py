import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Freedium"
    VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    STATIC_DIR: Path = BASE_DIR / "static"

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Medium scraper settings
    MEDIUM_COOKIES: str = os.getenv("MEDIUM_COOKIES", '')

    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    REDIS_TOKEN: str = os.getenv("REDIS_TOKEN", "")

settings = Settings()