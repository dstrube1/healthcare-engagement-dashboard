# middleware.py

"""Custom middleware for request logging and latency tracking."""

import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def request_timer(request: Request, call_next):
	start_time = time.time()
	response = await call_next(request)
	process_time = (time.time() - start_time) * 1000  # ms
	logger.info(f"{request.method} {request.url.path} completed in {process_time:.2f} ms")
	response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"
	return response
