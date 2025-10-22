# crud.py

"""Database and business logic operations for the Healthcare Engagement Dashboard."""

from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select
from app import models, schemas
import json, os

# Load compliance policies once at startup

POLICY_PATH = os.path.join(os.path.dirname(__file__), "compliance_policies.json")
if os.path.exists(POLICY_PATH):
	with open(POLICY_PATH, "r") as f:
		COMPLIANCE_POLICIES = json.load(f)
else:
	COMPLIANCE_POLICIES = {"rules": []}

# --- CRUD Functions ---

def get_physicians(session: Session, state: Optional[str] = None, specialty: Optional[str] = None) -> List[models.Physician]:
	query = select(models.Physician)
	if state:
		query = query.where(models.Physician.state == state)
	if specialty:
		query = query.where(models.Physician.specialty == specialty)
	return session.exec(query).all()

def get_messages(session: Session, physician_id: Optional[int] = None, start_ts: Optional[str] = None, end_ts: Optional[str] = None,) -> List[models.Message]:
	query = select(models.Message)
	if physician_id:
		query = query.where(models.Message.physician_id == physician_id)
	if start_ts:
		start = datetime.fromisoformat(start_ts)
		query = query.where(models.Message.timestamp >= start)
	if end_ts:
		end = datetime.fromisoformat(end_ts)
		query = query.where(models.Message.timestamp <= end)
	return session.exec(query).all()

def get_message(session: Session, message_id: int) -> Optional[models.Message]:
	return session.get(models.Message, message_id)

# --- Classification Logic ---

def classify_message(msg: models.Message) -> schemas.ClassificationResult:
	text = (msg.message_text or "").lower()
	triggered = []
	for rule in COMPLIANCE_POLICIES.get("rules", []):
		for kw in rule.get("keywords_any", []):
			if kw.lower() in text:
				triggered.append(
					schemas.ClassificationRule(
						id=rule.get("id"),
						name=rule.get("name"),
						action=rule.get("action"),
						requires_append=rule.get("requires_append"),
						keyword=kw,
					)
				)
				break
	return schemas.ClassificationResult(message_id=msg.message_id, triggered_rules=triggered)
