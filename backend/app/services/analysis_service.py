from app.detector.engine import DetectionEngine
from app.utils.feature_extractor import extract_features_from_text


class AnalysisService:
    """Service for essay analysis and insight generation."""

    def __init__(self) -> None:
        self.engine = DetectionEngine()

    async def analyze(self, essay: str) -> dict[str, object]:
        features = extract_features_from_text(essay)
        decision = self.engine.analyze_with_highlights(essay, features)
        prediction = "Likely AI Generated" if decision.overall_score >= 0.7 else "Suspicious" if decision.overall_score >= 0.4 else "Likely Human Written"
        confidence = round(decision.overall_score, 4)
        return {
            "prediction": prediction,
            "confidence": confidence,
            "summary": "This essay has been scored using linguistic patterns and perplexity signals.",
            "word_count": len(essay.split()),
            "character_count": len(essay),
            "status": "completed",
        }
