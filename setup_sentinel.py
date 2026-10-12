from pathlib import Path

ROOT = Path("backend")

FILES = {
    ROOT / "app" / "__init__.py": "",

    ROOT / "app" / "main.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Sentinel sustainability monitoring and action API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.cors_origins.split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "status": "running",
    }


@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
    }
''',

    ROOT / "app" / "config.py": '''from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sentinel API"
    app_env: str = "development"
    debug: bool = True

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # Supabase PostgreSQL
    database_url: str = ""

    # Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # Google Maps
    google_maps_api_key: str = ""

    # Frontend
    cors_origins: str = "http://localhost:5173"

    # Optional ML model
    model_path: str = "model/sentinel.joblib"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
''',

    ROOT / "app" / "database.py": '''from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
''',

    ROOT / "app" / "models.py": '''from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    building_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )


class Space(Base):
    __tablename__ = "spaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    space_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )


class Reading(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    space_id: Mapped[int] = mapped_column(
        ForeignKey("spaces.id"),
        nullable=False,
    )
    reading_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    resource: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reading_id: Mapped[int] = mapped_column(
        ForeignKey("readings.id"),
        nullable=False,
    )
    predicted_value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    anomaly_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prediction_id: Mapped[int | None] = mapped_column(
        ForeignKey("predictions.id"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="open",
        nullable=False,
    )


class Outcome(Base):
    __tablename__ = "outcomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_id: Mapped[int] = mapped_column(
        ForeignKey("actions.id"),
        nullable=False,
    )
    estimated_impact: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    verified_impact: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    recorded_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
''',

    ROOT / "app" / "schemas.py": '''from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class BuildingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    building_type: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class SpaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    building_id: int
    name: str
    space_type: str | None = None


class ReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    space_id: int
    reading_date: date
    resource: str
    value: float


class ActionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    prediction_id: int | None = None


class ActionResponse(ActionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str


class OutcomeCreate(BaseModel):
    action_id: int
    estimated_impact: float | None = None
    verified_impact: float | None = None
    notes: str | None = None


class AnomalyRequest(BaseModel):
    values: list[float] = Field(default_factory=list)


class ExplanationResponse(BaseModel):
    analysis: dict
    explanation: str
''',

    ROOT / "app" / "services.py": '''"""
Sentinel business logic.

Responsibilities:

- anomaly detection
- ML model inference
- deterministic fallback rules
- Gemini explanations
- recommendations
- impact calculations

The actual dataset-specific implementation will be connected after
the source CSV schema is inspected.
"""

from statistics import mean


def detect_anomaly(values: list[float]) -> dict:
    """
    Transparent fallback anomaly detector.

    Uses the previous observations as a baseline and compares the
    latest observation against that baseline.
    """

    if len(values) < 2:
        return {
            "is_anomaly": False,
            "score": 0.0,
            "baseline": None,
            "current": values[-1] if values else None,
        }

    previous = values[:-1]
    current = values[-1]

    baseline = mean(previous)

    if baseline == 0:
        return {
            "is_anomaly": False,
            "score": 0.0,
            "baseline": baseline,
            "current": current,
        }

    deviation = abs(current - baseline) / abs(baseline)

    return {
        "is_anomaly": deviation >= 0.30,
        "score": round(deviation, 4),
        "baseline": baseline,
        "current": current,
    }


def fallback_explanation(anomaly: dict) -> str:
    if not anomaly.get("is_anomaly"):
        return "No significant anomaly was detected."

    baseline = anomaly.get("baseline")
    current = anomaly.get("current")

    return (
        f"The latest reading ({current}) differs substantially from "
        f"the recent baseline ({baseline}). The space should be "
        "investigated for a possible operational or usage change."
    )


def generate_recommendation(anomaly: dict) -> str:
    if not anomaly.get("is_anomaly"):
        return "Continue monitoring the space."

    return (
        "Inspect the affected space, review recent operational changes, "
        "and verify the relevant equipment or usage pattern."
    )
''',

    ROOT / "app" / "routes.py": '''from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import Action, Building, Outcome, Reading, Space
from .schemas import (
    ActionCreate,
    ActionResponse,
    AnomalyRequest,
    BuildingResponse,
    ExplanationResponse,
    OutcomeCreate,
    ReadingResponse,
    SpaceResponse,
)
from .services import (
    detect_anomaly,
    fallback_explanation,
    generate_recommendation,
)


router = APIRouter(prefix="/api/v1")


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    return {
        "buildings": db.query(Building).count(),
        "spaces": db.query(Space).count(),
        "readings": db.query(Reading).count(),
        "status": "ok",
    }


# ---------------------------------------------------------------------------
# Buildings
# ---------------------------------------------------------------------------

@router.get(
    "/buildings",
    response_model=list[BuildingResponse],
)
def buildings(db: Session = Depends(get_db)):
    return db.scalars(
        select(Building).order_by(Building.name)
    ).all()


@router.get(
    "/map/buildings",
    response_model=list[BuildingResponse],
)
def map_buildings(db: Session = Depends(get_db)):
    buildings = db.scalars(
        select(Building).order_by(Building.name)
    ).all()

    return [
        building
        for building in buildings
        if building.latitude is not None
        and building.longitude is not None
    ]


# ---------------------------------------------------------------------------
# Spaces
# ---------------------------------------------------------------------------

@router.get(
    "/spaces",
    response_model=list[SpaceResponse],
)
def spaces(db: Session = Depends(get_db)):
    return db.scalars(
        select(Space).order_by(Space.name)
    ).all()


# ---------------------------------------------------------------------------
# Readings
# ---------------------------------------------------------------------------

@router.get(
    "/readings",
    response_model=list[ReadingResponse],
)
def readings(db: Session = Depends(get_db)):
    return db.scalars(
        select(Reading).order_by(Reading.reading_date.desc())
    ).all()


# ---------------------------------------------------------------------------
# Anomalies
# ---------------------------------------------------------------------------

@router.get("/anomalies")
def anomalies():
    return {
        "items": [],
        "message": "Anomalies are generated from Supabase readings.",
    }


@router.post("/anomalies/run")
def run_anomalies(
    data: AnomalyRequest,
):
    result = detect_anomaly(data.values)

    return {
        "analysis": result,
        "recommendation": generate_recommendation(result),
    }


# ---------------------------------------------------------------------------
# AI explanation
# ---------------------------------------------------------------------------

@router.post(
    "/ai/explain",
    response_model=ExplanationResponse,
)
def explain(data: AnomalyRequest):
    result = detect_anomaly(data.values)

    return {
        "analysis": result,
        "explanation": fallback_explanation(result),
    }


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

@router.get(
    "/actions",
    response_model=list[ActionResponse],
)
def get_actions(db: Session = Depends(get_db)):
    return db.scalars(
        select(Action).order_by(Action.id.desc())
    ).all()


@router.post(
    "/actions",
    response_model=ActionResponse,
)
def create_action(
    data: ActionCreate,
    db: Session = Depends(get_db),
):
    action = Action(
        title=data.title,
        description=data.description,
        prediction_id=data.prediction_id,
        status="open",
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    return action


@router.patch("/actions/{action_id}/complete")
def complete_action(
    action_id: int,
    db: Session = Depends(get_db),
):
    action = db.get(Action, action_id)

    if action is None:
        return {
            "status": "error",
            "message": "Action not found.",
        }

    action.status = "completed"

    db.commit()

    return {
        "status": "completed",
        "action_id": action_id,
    }


# ---------------------------------------------------------------------------
# Outcomes
# ---------------------------------------------------------------------------

@router.get("/outcomes")
def get_outcomes(db: Session = Depends(get_db)):
    return db.scalars(
        select(Outcome).order_by(Outcome.id.desc())
    ).all()


@router.post("/outcomes")
def create_outcome(
    data: OutcomeCreate,
    db: Session = Depends(get_db),
):
    outcome = Outcome(
        action_id=data.action_id,
        estimated_impact=data.estimated_impact,
        verified_impact=data.verified_impact,
        notes=data.notes,
    )

    db.add(outcome)
    db.commit()
    db.refresh(outcome)

    return outcome


# ---------------------------------------------------------------------------
# Impact
# ---------------------------------------------------------------------------

@router.get("/impact/summary")
def impact_summary(db: Session = Depends(get_db)):
    outcomes = db.scalars(select(Outcome)).all()

    estimated = sum(
        outcome.estimated_impact or 0
        for outcome in outcomes
    )

    verified = sum(
        outcome.verified_impact or 0
        for outcome in outcomes
    )

    return {
        "estimated_impact": estimated,
        "verified_impact": verified,
    }
''',

    ROOT / "scripts" / "import_data.py": '''"""
SENTINEL ONE-TIME DATA IMPORTER

Purpose:
    Import/transform the supplied source CSV into Supabase.

Important:
    The Sentinel backend does NOT read the CSV during normal operation.

Architecture:

    Source CSV
        ↓
    This script (one-time)
        ↓
    Supabase
        ↓
    Sentinel FastAPI
        ↓
    React frontend

The exact column mapping must be implemented against the actual
CSV supplied for the project. Do not invent mappings.
"""

from pathlib import Path


def main():
    csv_path = Path("data/sentinel.csv")

    if not csv_path.exists():
        print("Source CSV not found.")
        print()
        print("Place the supplied dataset at:")
        print("    data/sentinel.csv")
        print()
        print("Then implement the dataset-specific mapping.")
        return

    print(f"Found source CSV: {csv_path}")
    print()
    print("Dataset detected.")
    print(
        "The importer is intentionally waiting for the actual "
        "CSV schema before mapping columns into Supabase."
    )


if __name__ == "__main__":
    main()
''',

    ROOT / "tests" / "__init__.py": "",

    ROOT / "tests" / "test_api.py": '''from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "Sentinel API"


def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
''',

    ROOT / ".env.example": '''# ============================================================
# SENTINEL ENVIRONMENT VARIABLES
# ============================================================

# Application
APP_NAME=Sentinel API
APP_ENV=development
DEBUG=true

# ============================================================
# SUPABASE
# ============================================================

# Supabase project URL
SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co

# Supabase API key
#
# For backend-only Supabase operations, use the appropriate
# server-side key and NEVER expose it to the React frontend.
SUPABASE_KEY=YOUR_SUPABASE_KEY

# PostgreSQL connection used by FastAPI/SQLAlchemy
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@YOUR_DB_HOST:5432/postgres

# ============================================================
# GEMINI
# ============================================================

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

# ============================================================
# GOOGLE MAPS
# ============================================================

GOOGLE_MAPS_API_KEY=

# ============================================================
# FRONTEND
# ============================================================

CORS_ORIGINS=http://localhost:5173

# ============================================================
# OPTIONAL ML MODEL
# ============================================================

MODEL_PATH=model/sentinel.joblib
''',

    ROOT / ".gitignore": '''# Environment / secrets
.env

# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environments
.venv/
venv/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
''',

    ROOT / "requirements.txt": '''fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
pydantic
pydantic-settings
python-dotenv
pandas
numpy
scikit-learn
joblib
httpx
google-genai
python-multipart
pytest
''',

    ROOT / "README.md": '''# Sentinel Backend

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
''',
}


def create_project():
    print()
    print("=" * 60)
    print(" SENTINEL BACKEND SETUP")
    print("=" * 60)
    print()

    for path, content in FILES.items():
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            print(f"[SKIP]   {path}")
            continue

        path.write_text(content, encoding="utf-8")
        print(f"[CREATE] {path}")

    print()
    print("=" * 60)
    print(" SENTINEL BACKEND CREATED")
    print("=" * 60)
    print()
    print("Structure:")
    print()
    print("backend/")
    print("├── app/")
    print("│   ├── main.py")
    print("│   ├── config.py")
    print("│   ├── database.py")
    print("│   ├── models.py")
    print("│   ├── schemas.py")
    print("│   ├── services.py")
    print("│   └── routes.py")
    print("├── model/")
    print("├── scripts/")
    print("│   └── import_data.py")
    print("├── tests/")
    print("│   └── test_api.py")
    print("├── .env.example")
    print("├── .gitignore")
    print("├── requirements.txt")
    print("└── README.md")
    print()
    print("Next steps:")
    print("1. cd backend")
    print("2. Create your .env from .env.example")
    print("3. Add your Supabase credentials")
    print("4. Install requirements")
    print("5. Run the FastAPI server")
    print()
    print("The actual CSV schema still needs to be mapped once the")
    print("source CSV is available.")
    print()


if __name__ == "__main__":
    create_project()
