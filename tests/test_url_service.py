import pytest
from app.services.url_service import URLService

class TestURLService:
    def test_valid_url(self):
        assert URLService.is_valid_url("https://www.example.com") is True
        assert URLService.is_valid_url("http://example.com") is True
        assert URLService.is_valid_url("https://subdomain.example.com/path?param=value") is True

    def test_invalid_url(self):
        assert URLService.is_valid_url("not-a-url") is False
        assert URLService.is_valid_url("") is False
        assert URLService.is_valid_url("ftp://example.com") is False
        assert URLService.is_valid_url("just-text") is False

    def test_empty_url(self):
        assert URLService.is_valid_url("") is False
        assert URLService.is_valid_url(None) is False