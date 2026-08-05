from fastapi import APIRouter

from app.detector.engine import DetectionEngine
from app.utils.feature_extractor import extract_features_from_text

router = APIRouter(prefix="/api", tags=["detection"])
engine = DetectionEngine()


@router.post("/detect")
async def detect_text(payload: dict[str, str]) -> dict[str, object]:
    essay = payload.get("essay", "")
    features = extract_features_from_text(essay)
    decision = engine.analyze_with_highlights(essay, features)

    return {
        "overall_score": decision.overall_score,
        "sentence_highlights": [
            {
                "sentence": item.sentence,
                "score": item.score,
                "confidence": item.confidence,
                "status": item.status,
                "reasons": item.reasons,
                "extracted_features": item.extracted_features,
            }
            for item in decision.sentence_highlights
        ],
    }
