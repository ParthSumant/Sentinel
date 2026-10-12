"""
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
