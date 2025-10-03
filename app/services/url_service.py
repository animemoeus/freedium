import requests
import validators
from typing import Optional

class URLService:
    @staticmethod
    def is_valid_url(text: str) -> bool:
        if not text:
            return False
        try:
            return validators.url(text) is True
        except Exception:
            return False

    @staticmethod
    def get_url_data(url: str, timeout: int = 50) -> Optional[requests.Response]:
        if not URLService.is_valid_url(url):
            raise ValueError("Invalid URL provided")

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise e