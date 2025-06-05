from crewai import Agent
from tools import WebSearchTool, WebScraperTool
from models import (
    SearchQuery,
    SearchResults,
    ScrapeRequest,
    ScrapeResponse,
    ConsolidatedData,
    OfferAnalysisRequest,
    OfferAnalysisResponse
)

def create_search_specialist_agent():
    """
    DuckDuckGo Search Specialist Agent:
    - Input: SearchQuery (Pydantic)
    - Output: SearchResults (Pydantic)
    """
    return Agent(
        role='DuckDuckGo Search Specialist',
        goal='Generate a short, effective search string to query DuckDuckGo and use websearchtool to return a structured list of URLs.',
        backstory=(
            "You are an expert in formulating search engine queries for DuckDuckGo. "
            "You receive a SearchQuery Pydantic object containing the query details "
            "and return a SearchResults Pydantic object with the extracted URLs."
        ),
        tools=[WebSearchTool()],
        llm="azure/gpt-35-turbo",
        verbose=True
    )

def web_scrape_specialist_agent():
    """
    Web Scraper Agent:
    - Input: ScrapeRequest (Pydantic)
    - Output: ScrapeResponse (Pydantic)
    """
    return Agent(
        role='Web Scraper Specialist',
        goal='Scrape relevant information from a webpage and fill it into a structured Pydantic data class.',
        backstory=(
            "You are a skilled web scraper capable of extracting structured data from webpages. "
            "You receive a ScrapeRequest Pydantic object with the URL and extraction parameters, "
            "and return a ScrapeResponse Pydantic object containing the structured data."
        ),
        tools=[WebScraperTool()],
        llm="azure/gpt-35-turbo",
        verbose=True
    )

def consolidate_structured_data_agent():
    """
    Data Consolidator Agent:
    - Input: list of ScrapeResponse (Pydantic)
    - Output: ConsolidatedData (Pydantic)
    """
    return Agent(
        role='Data Consolidator Specialist',
        goal='Merge structured data from multiple sources into a unified, validated Pydantic data object.',
        backstory=(
            "You consolidate and validate structured data received from multiple sources. "
            "You handle missing or inconsistent data by either filling it intelligently or removing it as necessary. "
            "Input: List of ScrapeResponse Pydantic objects. Output: ConsolidatedData Pydantic object."
        ),
        llm="azure/gpt-35-turbo",
        verbose=True
    )

def create_competitive_offer_analyst_agent():
    """
    Competitive Offer Analyst Agent:
    - Input: OfferAnalysisRequest (Pydantic)
    - Output: OfferAnalysisResponse (Pydantic)
    """
    return Agent(
        role='Competitive Offer Analyst',
        goal='Analyze multiple structured offers and generate a competitive offer in Pydantic format.',
        backstory=(
            "You analyze structured data representing offers from various sources. "
            "You apply analytical reasoning to create a new competitive offer that is more relevant and appealing. "
            "Input: OfferAnalysisRequest Pydantic object. Output: OfferAnalysisResponse Pydantic object."
        ),
        llm="azure/gpt-35-turbo",
        verbose=True
    )
