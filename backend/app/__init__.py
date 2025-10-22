# __init__.py

"""Backend app package initializer.

This file allows the FastAPI app to be imported as a Python module, e.g., from app.main import app. It can also perform shared setup logic for the package (like loading env vars or setting up logging). """

import logging 
import os 
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Configure base logger
logging.basicConfig( level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", )
logger = logging.getLogger(__name__) 
logger.info("Initialized app package.")