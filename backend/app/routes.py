from fastapi import APIRouter, Depends
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
