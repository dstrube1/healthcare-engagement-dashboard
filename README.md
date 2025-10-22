# healthcare-engagement-dashboard
**Impiricus - Full Stack Engineer - Take-Home Assignment - Healthcare Engagement Dashboard**

This repository scaffolds a minimal FastAPI backend + React frontend that satisfies these requirements: 
* load physician + message data
* expose clean APIs
* simple compliance classification
* SQLite storage
* unit test
* request logging with latency
* Dockerfile
* README

# Project layout

![Project layout](https://github.com/dstrube1/healthcare-engagement-dashboard/blob/main/hed-project-layout.png)

# Backend (FastAPI) — highlights

* Uses SQLModel (built on SQLAlchemy) with SQLite by default (configurable via DATABASE_URL).
* Endpoints implemented:
* * GET /physicians — filters: state, specialty (query params).
* * GET /messages — filters: physician_id, start_ts, end_ts (ISO datetimes).
* * POST /classify/{message_id} — loads compliance_policies.json and matches keyword-based rules against the message text; returns the triggered rules.
* Request logging middleware that logs method/path, status, and latency in milliseconds.
* A simple CRUD layer and Pydantic schemas for clean separation.

# Frontend (React) — highlights
* Minimal single-page React app (Vite-style entry) that:
* * Allows filtering messages by physician_id.
* * Shows a table of messages (timestamp, topic, sentiment) and a "Classify" button per row.
* * When "Classify" is clicked, POSTs to /classify/{message_id} and displays the rule(s) triggered.

# Deployment
* backend/Dockerfile builds the FastAPI app using uvicorn.
* .env.example contains DATABASE_URL and APP_PORT variables.

# How to use (local)

1. Backend (dev):

` # from backend/ `
` python3 -m venv .venv `
` source .venv/bin/activate `
` pip install -r requirements.txt `
` # create DB and load CSVs programmatically (helper endpoint exists in main.py) `
` uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 `

2. Frontend (dev):

` cd frontend `
` npm install `
` npm run dev `
` # open http://localhost:5173 ` 

3. Docker (backend only):

` # from backend/ `
` docker build -t hed-backend:latest . `
` docker run --env-file .env.example -p 8000:8000 hed-backend:latest `

OR

` docker build -t hed-backend . `
` docker run -p 8000:8000 hed-backend `


