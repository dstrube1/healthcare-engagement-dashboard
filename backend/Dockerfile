# backend/Dockerfile

# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and data
COPY app ./app
COPY data ./data

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL=sqlite:///./hed.db

# Ensure database is initialized at container start (optional)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
