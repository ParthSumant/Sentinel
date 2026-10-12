from datetime import date, datetime

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
