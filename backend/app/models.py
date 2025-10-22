# models.py

# backend/app/models.py

"""Database models using SQLModel for the Healthcare Engagement Dashboard."""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Physician(SQLModel, table=True):
	__tablename__ = "physicians"
	physician_id: int = Field(primary_key=True)
	npi: Optional[str] = None
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	specialty: Optional[str] = None
	state: Optional[str] = None
	consent_opt_in: Optional[bool] = None
	preferred_channel: Optional[str] = None

class Message(SQLModel, table=True):
	__tablename__ = "messages"
	message_id: int = Field(primary_key=True)
	physician_id: int = Field(foreign_key="physicians.physician_id")
	channel: Optional[str] = None
	direction: Optional[str] = None
	timestamp: datetime
	message_text: str
	campaign_id: Optional[str] = None
	topic: Optional[str] = None
	compliance_tag: Optional[str] = None
	sentiment: Optional[str] = None
	delivery_status: Optional[str] = None
	response_latency_sec: Optional[int] = None













