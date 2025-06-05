from fastapi import APIRouter, HTTPException
from models import ChatRequest
from workflow import run_offer_analysis_crew
from config import logger
from datetime import datetime

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    logger.info(f"Received chat request: {request.tenantName}")
    if not request.tenantName or not request.offerType:
        raise HTTPException(status_code=400, detail="tenantName and offerType are required.")
    result = run_offer_analysis_crew(request)
    if result.get("status") == "failed":
        raise HTTPException(status_code=500, detail=result.get("error"))
    return {"response": result, "status": "success"}

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "framework": "CrewAI",
        "timestamp": datetime.now().isoformat()
    }
