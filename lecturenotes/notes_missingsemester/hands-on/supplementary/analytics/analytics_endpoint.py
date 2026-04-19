"""
analytics_endpoint.py — Boilerplate /analytics endpoint for Block 9

This file contains the analytics route and helper function that students
deploy in Block 9. They do not write these queries — the focus is on
interpreting the results and understanding what the numbers tell them.

Integration:
    Copy the route into app/main.py and import the helper.
    Or: import this module and include the router.

Usage:
    curl https://192.168.56.11/api/analytics -k -H "X-API-Key: your-key"
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

# These imports assume the standard PixelWise project structure.
# Adjust if your module layout differs.
# from app.models import Prediction
# from app.main import get_db, verify_api_key

router = APIRouter()


def compute_analytics(db: Session, Prediction):
    """
    Query the predictions table and return summary analytics.

    Returns a dict with:
        - total_predictions: int
        - predictions_per_class: {digit: count, ...}
        - avg_confidence: float or null
        - model_versions: {version: count, ...}
    """
    # Total predictions
    total = db.query(func.count(Prediction.id)).scalar() or 0

    # Predictions per class
    per_class_rows = (
        db.query(Prediction.prediction, func.count(Prediction.id))
        .group_by(Prediction.prediction)
        .order_by(Prediction.prediction)
        .all()
    )
    predictions_per_class = {row[0]: row[1] for row in per_class_rows}

    # Average confidence (may be NULL if no confidence values stored yet)
    avg_conf = db.query(func.avg(Prediction.confidence)).scalar()
    avg_confidence = round(float(avg_conf), 4) if avg_conf is not None else None

    # Model version breakdown
    version_rows = (
        db.query(Prediction.model_version, func.count(Prediction.id))
        .group_by(Prediction.model_version)
        .order_by(Prediction.model_version)
        .all()
    )
    model_versions = {row[0]: row[1] for row in version_rows}

    return {
        "total_predictions": total,
        "predictions_per_class": predictions_per_class,
        "avg_confidence": avg_confidence,
        "model_versions": model_versions,
    }


# ----------------------------------------------------------------
# Example route — paste into app/main.py or include as a router
# ----------------------------------------------------------------
#
# @app.get("/api/analytics")
# def analytics(
#     db: Session = Depends(get_db),
#     _: str = Depends(verify_api_key),
# ):
#     from app.models import Prediction
#     return compute_analytics(db, Prediction)
