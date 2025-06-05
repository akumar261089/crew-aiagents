import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote, urlparse, parse_qs
import re
from typing import List, Dict, Any
from crewai.tools import BaseTool
from config import logger

class WebSearchTool(BaseTool):
    name: str = "DuckDuckGoSearch"
    description: str = "Performs a web search using DuckDuckGo and returns a list of URLs."

    def _run(self, query: str) -> List[str]:
        logger.info(f"Searching: {query}")
        encoded_query = quote(query.replace('"', ''))
        search_url = f"https://html.duckduckgo.com/html?q={encoded_query}"
        try:
            response = requests.get(search_url, headers={'User-Agent': 'Mozilla'}, timeout=100)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [
                link['href'] for link in soup.find_all('a', href=True)
                if re.match(r'^https?://', link['href']) and 'duckduckgo.com' not in link['href']
            ]
            return links[:10]
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []

class WebScraperTool(BaseTool):
    name: str = "WebScraper"
    description: str = "Scrapes a URL for content."

    def _run(self, url: str) -> Dict[str, Any]:
        logger.info(f"Scraping: {url}")
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla'}, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return {
                'url': url,
                'title': soup.title.string.strip() if soup.title else "No Title",
                'paragraphs': [
                    p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 20
                ][:5]
            }
        except Exception as e:
            logger.error(f"Scrape failed: {str(e)}")
            return {'error': str(e), 'url': url}
