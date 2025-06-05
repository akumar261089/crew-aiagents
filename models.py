from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Any

class ChatRequest(BaseModel):
    tenantName: str
    tenantDetails: str
    offerForm: List[Any]
    offerType: str
    existingOffers: List[str]
    metadata: str

# -------------------------------
# Additional Models
# -------------------------------

class SearchQuery(BaseModel):
    """
    Represents a search query string or parameters for the Search Specialist agent.
    """
    query: str = Field(..., description="The search term or question to search.")
    max_results: Optional[int] = Field(default=10, description="Maximum number of search results to return.")

class SearchResultItem(BaseModel):
    """
    Represents a single search result item with URL and optional metadata.
    """
    url: HttpUrl


class SearchResults(BaseModel):
    """
    Represents a list of search results.
    """
    results: List[SearchResultItem]

class ScrapeRequest(BaseModel):
    """
    Represents the request for the WebScraper agent.
    """
    url: HttpUrl
    selectors: Optional[List[str]] = Field(None, description="List of CSS selectors or XPaths to extract specific data.")
    context: Optional[Any] = Field(None, description="Optional context or instructions for the scraper.")

class ScrapeResponse(BaseModel):
    """
    Represents the structured scraped data from the webpage.
    """
    url: HttpUrl
    data: dict = Field(..., description="Scraped data as key-value pairs.")

class ConsolidatedData(BaseModel):
    """
    Represents the consolidated data after merging multiple ScrapeResponses.
    """
    consolidated_items: List[dict] = Field(..., description="List of structured items merged from different sources.")
    summary: Optional[str] = Field(None, description="Optional summary of the consolidated data.")

class OfferAnalysisRequest(BaseModel):
    """
    Represents the input for offer analysis.
    """
    offers: List[dict] = Field(..., description="List of offers with their details (each offer should be a dict).")
    tenant_context: Optional[str] = Field(None, description="Contextual information about the tenant or target audience.")

class OfferAnalysisResponse(BaseModel):
    """
    Represents the analyzed competitive offer.
    """
    recommended_offer: dict = Field(..., description="Recommended competitive offer details as structured data.")
    rationale: Optional[str] = Field(None, description="Explanation of why this offer was recommended.")
