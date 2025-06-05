from crewai import Crew, Process
from pydantic import ValidationError
import json
from config import logger
from models import (
    ChatRequest,
    SearchResults,
    ScrapeResponse,
    ConsolidatedData,
    OfferAnalysisResponse
)
from tasks import (
    create_search_task,
    create_scrape_task,
    create_consolidation_task,
    create_offer_analysis_task
)
from datetime import datetime
def parse_model_output(output, model_class):
    """
    Helper to parse raw string output from a CrewAgent into a Pydantic model.
    """
    if isinstance(output, model_class):
        return output
    if hasattr(output, 'raw'):
        raw_output = output.raw
    else:
        raw_output = output

    try:
        # Try parsing JSON directly
        parsed = json.loads(raw_output)
        return model_class(**parsed)
    except (json.JSONDecodeError, TypeError):
        # Fallback: parse manually if the LLM wrapped it in code block or prefix
        try:
            raw_output = raw_output.strip()
            if raw_output.startswith("```") and raw_output.endswith("```"):
                raw_output = raw_output.strip("`").strip()
            # Remove any extra labels like "ScrapeResponse:"
            if ":" in raw_output:
                raw_output = raw_output.split(":", 1)[1].strip()
            parsed = json.loads(raw_output)
            return model_class(**parsed)
        except Exception as e:
            raise ValidationError(f"Could not parse output into {model_class.__name__}: {e}")

def run_offer_analysis_crew(request: ChatRequest):
    logger.info(f"Starting CrewAI workflow for tenant: {request.tenantName}")
    try:
        ### STEP 1: Search for competitor URLs
        search_task = create_search_task(
            query=f"{request.tenantName} {request.offerType} {request.tenantDetails}",
            max_results=10
        )
        search_agent = search_task.agent
        crew = Crew(
            agents=[search_agent],
            tasks=[search_task],
            process=Process.sequential,
            verbose=True
        )
        search_results_raw = crew.kickoff()
        search_results = SearchResults.parse_obj(search_results_raw)
        # Parse SearchResults
        search_results = SearchResults.model_validate_json(search_results.raw)

        logger.info(f"Search results: {search_results.urls}")

        ### STEP 2: Web scraping of each URL in parallel
        scrape_tasks = [
            create_scrape_task(url_result,request.offerForm)
            for url_result in search_results
        ]
        logger.info(f"Created {scrape_tasks} scrape tasks for URLs.")
        scrape_agents = [task.agent for task in scrape_tasks]
        crew = Crew(
            agents=scrape_agents,
            tasks=scrape_tasks,
            process=Process.concurrent,  # Run in parallel
            verbose=True
        )
        crew_output  = crew.kickoff()
        scrape_response = parse_model_output(crew_output, ScrapeResponse)
        scrape_responses = [
            ScrapeResponse.parse_obj(resp) for resp in scrape_response
        ]
        logger.info(f"Scraped {len(scrape_responses)} pages successfully.")

        ### Optional: Store the scraped data somewhere
        store_scraped_data(scrape_responses, request.tenantName)

        ### STEP 3: Consolidate structured data
        consolidation_task = create_consolidation_task(scrape_responses)
        consolidation_agent = consolidation_task.agent
        crew = Crew(
            agents=[consolidation_agent],
            tasks=[consolidation_task],
            process=Process.sequential,
            verbose=True
        )
        consolidated_data_raw = crew.kickoff()
        consolidated_data = ConsolidatedData.parse_obj(consolidated_data_raw)
        logger.info(f"Consolidated data: {consolidated_data}")

        ### STEP 4: Analyze competitive offer
        offer_analysis_task = create_offer_analysis_task(
            offers=consolidated_data.data,
            tenant_context=request.tenantDetails
        )
        offer_analysis_agent = offer_analysis_task.agent
        crew = Crew(
            agents=[offer_analysis_agent],
            tasks=[offer_analysis_task],
            process=Process.sequential,
            verbose=True
        )
        offer_analysis_raw = crew.kickoff()
        offer_analysis = OfferAnalysisResponse.parse_obj(offer_analysis_raw)
        logger.info(f"Generated competitive offer analysis: {offer_analysis}")

        return {
            "tenantName": request.tenantName,
            "analysis": offer_analysis.dict(),
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Workflow error: {str(e)}")
        return {"error": str(e), "status": "failed", "timestamp": datetime.now().isoformat()}


def store_scraped_data(scrape_responses: list[ScrapeResponse], tenant_name: str):
    """
    Example function to store scraped data.
    For now, we just log it. You can extend it to store in a DB, S3, etc.
    """
    logger.info(f"Storing scraped data for tenant: {tenant_name}")
    for idx, response in enumerate(scrape_responses, 1):
        logger.debug(f"Scraped Data {idx}: {response.json()}")
