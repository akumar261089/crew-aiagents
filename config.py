import os
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Azure OpenAI configuration
ENDPOINT = os.getenv("AZURE_API_BASE")
MODEL_NAME = os.getenv("MODEL_NAME")

SUBSCRIPTION_KEY = os.getenv("AZURE_API_KEY")
API_VERSION = os.getenv("AZURE_API_VERSION")

# Validate API key
if SUBSCRIPTION_KEY is None:
    logger.error("Azure API key is missing. Please set the AZURE_API_KEY environment variable.")
    raise ValueError("Azure API key is missing.")


