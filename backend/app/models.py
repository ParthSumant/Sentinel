from datetime import date, datetime

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
