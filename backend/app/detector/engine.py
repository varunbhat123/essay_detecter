from __future__ import annotations

from app.detector.scoring import EssayDecision, SentenceScorer
from app.models.detection import DetectionResult
from app.models.features import EssayFeatures


class DetectionEngine:
    """Explainable AI-likelihood engine built from linguistic signals only."""

    def __init__(self, model_name: str = "gpt2") -> None:
        self.scorer = SentenceScorer(model_name=model_name)

    def analyze(self, text: str, features: EssayFeatures) -> EssayDecision:
        sentences = [item.sentence_text for item in features.sentence_features]
        return self.scorer.score_essay(sentences, features.sentence_features)

    def analyze_with_highlights(self, text: str, features: EssayFeatures) -> DetectionResult:
        sentences = [item.sentence_text for item in features.sentence_features]
        return self.scorer.score_with_highlights(sentences, features.sentence_features)
