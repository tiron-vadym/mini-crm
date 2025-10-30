#!/bin/sh
set -e

echo "Waiting for database to start..."
sleep 5

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
