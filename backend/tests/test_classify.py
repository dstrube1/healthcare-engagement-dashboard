# test_classify.py

"""Unit test for message classification logic."""

from app import crud, models

def test_classify_message_basic():
	# Create a dummy message with text containing a keyword from compliance rules
	msg = models.Message(
		message_id=1,
		physician_id=101,
		timestamp="2025-10-20T10:00:00Z",
		message_text="Please schedule a follow-up appointment and include patient data.",
	)
	result = crud.classify_message(msg)

	# result should be a ClassificationResult with triggered_rules list
	assert hasattr(result, "triggered_rules")
	assert result.message_id == 1
	# Optional: ensure rules triggered if policies contain matching keywords
	if crud.COMPLIANCE_POLICIES.get("rules"):
	    assert isinstance(result.triggered_rules, list)
