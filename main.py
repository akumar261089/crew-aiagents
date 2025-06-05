from fastapi import FastAPI
from routes import router
from config import logger

app = FastAPI(title="CrewAI Offer Management API", version="1.0.0")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "CrewAI API is running."}

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down CrewAI application.")
