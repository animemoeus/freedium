import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from app.config import settings
from app.services.url_service import URLService


class MediumScraper:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://medium.com/',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        }

        if settings.MEDIUM_COOKIES:
            self.headers['Cookie'] = settings.MEDIUM_COOKIES

    def scrape_article(self, url: str) -> Dict[str, Any]:
        if not URLService.is_valid_url(url):
            raise ValueError("Invalid URL provided")

        if "medium.com" not in url:
            raise ValueError("URL must be from medium.com")

        try:
            response = requests.get(url, headers=self.headers, timeout=30)

            if not response.ok:
                raise Exception(f"Failed to get the data with error response code: {response.status_code}")

            soup = BeautifulSoup(response.text, 'lxml')

            return self._extract_article_data(soup, url)

        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Scraping failed: {str(e)}")

    def _extract_article_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        article_data = {
            "url": url,
            "title": None,
            "author": None,
            "publication_date": None,
            "content": None,
            "content_html": None,
            "tags": [],
            "claps": None,
            "reading_time": None
        }

        # Extract title
        title_selectors = [
            'h1[data-testid="storyTitle"]',
            'h1',
            '.graf--title',
            'article h1'
        ]

        for selector in title_selectors:
            title_element = soup.select_one(selector)
            if title_element:
                article_data["title"] = title_element.get_text(strip=True)
                break

        # Extract author
        author_selectors = [
            '[data-testid="authorName"]',
            '.author-name',
            '[rel="author"]',
            '.js-userLink'
        ]

        for selector in author_selectors:
            author_element = soup.select_one(selector)
            if author_element:
                article_data["author"] = author_element.get_text(strip=True)
                break

        # Extract raw article HTML
        article_elements = soup.find_all('article')
        if article_elements:
            article_html = str(article_elements[0])
            article_data["content_html"] = article_html

            # Also extract plain text for fallback
            article_text = article_elements[0].get_text(strip=True)
            article_data["content"] = article_text

        # Extract reading time
        reading_time_selectors = [
            '[data-testid="storyReadTime"]',
            '.readingTime',
            'span[title*="read"]'
        ]

        for selector in reading_time_selectors:
            time_element = soup.select_one(selector)
            if time_element:
                article_data["reading_time"] = time_element.get_text(strip=True)
                break

        # Extract tags
        tag_selectors = [
            '[data-testid="storyTags"] a',
            '.tags a',
            '.js-tagButton'
        ]

        for selector in tag_selectors:
            tag_elements = soup.select(selector)
            if tag_elements:
                article_data["tags"] = [tag.get_text(strip=True) for tag in tag_elements]
                break

        return article_data