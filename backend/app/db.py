# db.py

"""Database setup and session utilities for the Healthcare Engagement Dashboard."""

import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL (defaults to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hed.db")

enable_sqlite_foreign_keys = DATABASE_URL.startswith("sqlite")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
	"""Create all database tables."""
	from app import models  # ensure models imported
	SQLModel.metadata.create_all(engine)
	
	if enable_sqlite_foreign_keys:
		with engine.connect() as conn:
			conn.exec_driver_sql("PRAGMA foreign_keys=ON;")
	
def get_session() -> Session:
	"""Provide a SQLModel session context."""
	return Session(engine)
