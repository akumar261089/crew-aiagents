from crewai import Task
from agents import (
    create_search_specialist_agent,
    web_scrape_specialist_agent,
    consolidate_structured_data_agent,
    create_competitive_offer_analyst_agent
)
from models import (
    SearchQuery,
    SearchResults,
    ScrapeRequest,
    ScrapeResponse,
    ConsolidatedData,
    OfferAnalysisRequest,
    OfferAnalysisResponse
)

# Task: Search Task - triggers Search Specialist Agent
def create_search_task(query: str, max_results: int = 10):
    return Task(
        description=(
            f"Use DuckDuckGo Search Specialist to search for: '{query}' "
            f"and run the tool with query string."
        ),
        expected_output=f"SearchResults (list of up to {max_results} URLs with titles and snippets).",
        agent=create_search_specialist_agent(),
        input_model=SearchQuery(query=query, max_results=max_results),
        output_model=SearchResults
    )

# Task: Scrape Task - triggers Web Scraper Agent
def create_scrape_task(url: str, offerform: list[str], selectors: list[str] = None):
    """
    Creates a scrape task that instructs the web scraper agent to extract
    the fields specified in 'offerform' from the given URL.
    """
    description = (
        f"Use Web Scraper to extract the following fields from {url}: {', '.join(offerform)}. "
        "Use CSS selectors or other scraping techniques to fill these fields. "
        "Return the result as a ScrapeResponse Pydantic object with key-value pairs."
    )
    return Task(
        description=description,
        expected_output="ScrapeResponse (structured scraped data).",
        agent=web_scrape_specialist_agent(),
        input_model=ScrapeRequest(url=url, selectors=selectors or offerform),  # pass offerform as selectors
        output_model=ScrapeResponse
    )

# Task: Consolidation Task - triggers Data Consolidation Agent
def create_consolidation_task(scrape_responses: list[ScrapeResponse]):
    return Task(
        description=(
            "Consolidate structured data from multiple scrape responses "
            "into a unified dataset."
        ),
        expected_output="ConsolidatedData (merged structured data with summary).",
        agent=consolidate_structured_data_agent(),
        input_model={"scrape_responses": [resp.dict() for resp in scrape_responses]},
        output_model=ConsolidatedData
    )

# Task: Offer Analysis Task - triggers Competitive Offer Analyst Agent
def create_offer_analysis_task(offers: list[dict], tenant_context: str = None):
    return Task(
        description=(
            "Analyze the structured data of multiple different offers "
            "to generate a competitive offer with more relevance."
        ),
        expected_output="OfferAnalysisResponse (recommended competitive offer).",
        agent=create_competitive_offer_analyst_agent(),
        input_model=OfferAnalysisRequest(offers=offers, tenant_context=tenant_context),
        output_model=OfferAnalysisResponse
    )
