# Sentinel Backend

Backend API for the Sentinel campus sustainability application.

## Architecture

The supplied dataset is used as a source for a one-time import.

    Source CSV
        |
        | one-time import / transformation
        v
    Supabase
        |
        v
    Sentinel FastAPI backend
        |
        | REST API
        v
    React frontend

The deployed/runtime backend does NOT read the CSV directly.

## Backend responsibilities

- REST API
- Supabase persistence
- Campus/building/space data
- Resource readings
- Anomaly detection
- ML inference when available
- Transparent deterministic fallback
- Gemini explanations
- Recommended corrective actions
- Persistent actions
- Outcomes
- Estimated vs verified impact
- Google Maps building data
- API documentation

## Project setup

Create a virtual environment:

    python -m venv .venv

Activate the environment and install dependencies:

    pip install -r requirements.txt

Create `.env` from `.env.example`:

    cp .env.example .env

On Windows PowerShell:

    Copy-Item .env.example .env

Add the actual Supabase credentials and other API keys to `.env`.

## Run the API

From the backend directory:

    uvicorn app.main:app --reload

API:

    http://127.0.0.1:8000

Interactive API documentation:

    http://127.0.0.1:8000/docs

## Dataset import

The source CSV is used only for the one-time data import.

It should NOT be read by the normal API runtime.

The importer is:

    scripts/import_data.py

The exact mapping should be implemented against the actual supplied
CSV schema.

## Security

Never commit `.env`.

Never put server-side secrets into the React frontend.

The repository should contain `.env.example`, not `.env`.
