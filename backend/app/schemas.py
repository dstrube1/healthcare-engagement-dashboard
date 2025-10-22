# schemas.py

"""Pydantic/SQLModel schemas for request and response models."""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel

class PhysicianBase(SQLModel):
	physician_id: int
	npi: Optional[str]
	first_name: Optional[str]
	last_name: Optional[str]
	specialty: Optional[str]
	state: Optional[str]
	consent_opt_in: Optional[bool]
	preferred_channel: Optional[str]

# orm_mode enabled for easy database serialization
class Physician(PhysicianBase): 
	class Config: orm_mode = True

class MessageBase(SQLModel):
	message_id: int
	physician_id: int
	channel: Optional[str]
	direction: Optional[str]
	timestamp: datetime
	message_text: str
	campaign_id: Optional[str]
	topic: Optional[str]
	compliance_tag: Optional[str]
	sentiment: Optional[str]
	delivery_status: Optional[str]
	response_latency_sec: Optional[int]

class Message(MessageBase): 
	class Config: orm_mode = True

class ClassificationRule(SQLModel):
	id: Optional[str]
	name: Optional[str]
	action: Optional[str]
	requires_append: Optional[str]
	keyword: Optional[str]

class ClassificationResult(SQLModel):
	message_id: int
	triggered_rules: List[ClassificationRule]
