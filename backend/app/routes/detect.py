from fastapi import APIRouter

from app.detector.engine import DetectionEngine
from app.models.detect import DetectRequest, DetectResponse
from app.utils.feature_extractor import extract_features_from_text

router = APIRouter(prefix="/api", tags=["detection"])
engine = DetectionEngine()


def _map_prediction(score: float) -> tuple[str, float, str]:
    if score >= 0.6:
        return "Likely AI Generated", score, "High AI-like signal across sentences; this remains a heuristic indicator, not proof of authorship."
    if score >= 0.35:
        return "Suspicious", score, "Mixed signals with moderate AI-like patterns; review is recommended."
    return "Likely Human Written", score, "Sentence-level patterns are consistent with authentic writing, though this is still a heuristic indicator."


@router.post("/detect", response_model=DetectResponse)
async def detect_text(payload: DetectRequest) -> DetectResponse:
    essay = payload.essay
    features = extract_features_from_text(essay)
    decision = engine.analyze_with_highlights(essay, features)
    prediction, confidence, summary = _map_prediction(decision.overall_score)
    return DetectResponse(
        overall_score=decision.overall_score,
        prediction=prediction,
        confidence=confidence,
        status="completed",
        summary=summary,
        sentence_highlights=[
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
    )
