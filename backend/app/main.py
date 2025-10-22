# main.py

"""FastAPI main entrypoint for the Healthcare Engagement Dashboard backend."""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_session, init_db
from app import crud, schemas
from app.middleware import request_timer
import logging
import pandas as pd
import os
import datetime

app = FastAPI(title="Healthcare Engagement Dashboard API", version="1.0.0")

# CORS (allow localhost frontend)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
	)

# Middleware for logging latency
app.middleware("http")(request_timer)

# Logger
logger = logging.getLogger(__name__)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
	logger.info("Initializing database...")
	init_db()

# --- API Endpoints ---

@app.get("/physicians", response_model=list[schemas.Physician])
def get_physicians(state: str | None = Query(None), specialty: str | None = Query(None)):
	"""List physicians, optionally filtered by state or specialty."""
	with get_session() as session:
		return crud.get_physicians(session, state=state, specialty=specialty)

@app.get("/messages", response_model=list[schemas.Message])
def get_messages(physician_id: int | None = Query(None), start_ts: str | None = Query(None), end_ts: str | None = Query(None),):
	"""List messages, optionally filtered by physician_id and date range."""
	with get_session() as session:
		return crud.get_messages(session, physician_id=physician_id, start_ts=start_ts, end_ts=end_ts)

@app.post("/classify/{message_id}", response_model=schemas.ClassificationResult)
def classify_message(message_id: int):
	"""Classify a message based on compliance policies."""
	with get_session() as session:
		msg = crud.get_message(session, message_id)
		if not msg:
			raise HTTPException(status_code=404, detail="Message not found")
		result = crud.classify_message(msg)
		return result

@app.post("/import")
def import_data(physicians_path: str = "./data/physicians.csv", messages_path: str = "./data/messages.csv"):
	"""Import physicians and messages CSV files into the database."""
	from app import models
	if not os.path.exists(physicians_path) or not os.path.exists(messages_path):
		raise HTTPException(status_code=400, detail="CSV files not found.")
	with get_session() as session:
		# Import physicians
		phys_df = pd.read_csv(physicians_path)
		for _, row in phys_df.iterrows():
			p = models.Physician(**row.to_dict())
			session.merge(p)
		
		# Import messages
		"""OLD: bad datetime logic
		msg_df = pd.read_csv(messages_path)
		for _, row in msg_df.iterrows():
			m = models.Message(**row.to_dict())
			session.merge(m)
		
		NEW: better datetime logic:
		"""
		msg_df = pd.read_csv(messages_path)
		for _, row in msg_df.iterrows():
			data = row.to_dict()
			# Convert timestamp if it's a string
			if isinstance(data.get("timestamp"), str):
				try:
					data["timestamp"] = datetime.datetime.fromisoformat(
						data["timestamp"].replace("Z", "+00:00")
					)
				except Exception:
					# fallback: try pandas parsing
					data["timestamp"] = pd.to_datetime(data["timestamp"]).to_pydatetime()
			m = models.Message(**data)
			session.merge(m)		
		
		session.commit()
	
	logger.info("Imported CSV data successfully.")
	return {"status": "success", "physicians": len(phys_df), "messages": len(msg_df)}

@app.get("/health")
def health_check():
	return {"status": "ok"}
















