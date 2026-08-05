from __future__ import annotations

from dataclasses import dataclass, field

from app.models.detection import DetectionResult, SentenceHighlight
from app.models.features import SentenceFeature
from app.utils.perplexity import LocalPerplexityCalculator


@dataclass
class SentenceDecision:
    sentence: str
    score: float
    reasons: list[str] = field(default_factory=list)


@dataclass
class EssayDecision:
    overall_score: float
    sentence_scores: list[SentenceDecision] = field(default_factory=list)


class SentenceScorer:
    """Heuristic scoring engine for explainable sentence-level AI likelihood.

    The detector does not ask an LLM whether the text is AI. It combines signal
    features such as perplexity, lexical richness, burstiness, entropy, etc. into
    a weighted numeric score.
    """

    def __init__(self, model_name: str = "gpt2") -> None:
        self.perplexity_calculator = LocalPerplexityCalculator(model_name=model_name)

    def _score_component(self, value: float, low: float, high: float) -> float:
        if high <= low:
            return 0.0
        clipped = max(low, min(value, high))
        return (clipped - low) / (high - low)

    def _determine_status(self, score: float) -> str:
        if score >= 0.7:
            return "likely_ai"
        if score >= 0.4:
            return "suspicious"
        return "likely_human"

    def score_sentence(self, sentence: str, features: SentenceFeature) -> SentenceDecision:
        perplexity = self.perplexity_calculator.score_sentence(sentence).perplexity

        reasons: list[str] = []
        weighted_signals: list[tuple[float, float]] = []

        perplexity_score = self._score_component(perplexity, 0.0, 200.0)
        weighted_signals.append((perplexity_score, 0.22))
        if perplexity > 120:
            reasons.append("High perplexity relative to reference language patterns")

        burstiness_score = self._score_component(features.burstiness, 0.0, 1.5)
        weighted_signals.append((burstiness_score, 0.12))
        if features.burstiness > 0.7:
            reasons.append("Unusual repetition burst pattern")

        vocab_score = self._score_component(features.vocabulary_diversity, 0.0, 1.0)
        weighted_signals.append((vocab_score, 0.10))
        if features.vocabulary_diversity > 0.75:
            reasons.append("Strong vocabulary diversity")

        readability_score = max(0.0, 1.0 - min(1.0, abs(features.readability_score - 60.0) / 80.0))
        weighted_signals.append((readability_score, 0.10))
        if features.readability_score < 40:
            reasons.append("Readability is unusually constrained or dense")

        entropy_score = self._score_component(features.entropy, 0.0, 4.0)
        weighted_signals.append((entropy_score, 0.08))
        if features.entropy > 2.8:
            reasons.append("High token unpredictability")

        repeated_phrase_score = self._score_component(features.repeated_phrase_ratio, 0.0, 0.5)
        weighted_signals.append((repeated_phrase_score, 0.10))
        if features.repeated_phrase_ratio > 0.15:
            reasons.append("Repeated phrase pattern detected")

        transition_score = self._score_component(features.transition_word_frequency, 0.0, 0.4)
        weighted_signals.append((transition_score, 0.08))
        if features.transition_word_frequency > 0.1:
            reasons.append("Transition wording is elevated")

        rhythm_score = self._score_component(features.sentence_complexity, 0.0, 3.0)
        weighted_signals.append((rhythm_score, 0.10))
        if features.sentence_complexity > 1.4:
            reasons.append("Sentence rhythm is unusually patterned or complex")

        lexical_score = self._score_component(features.lexical_richness, 0.0, 1.0)
        weighted_signals.append((lexical_score, 0.10))
        if features.lexical_richness > 0.7:
            reasons.append("Lexical richness is elevated")

        total_weight = sum(weight for _, weight in weighted_signals)
        combined_score = sum(signal * weight for signal, weight in weighted_signals) / total_weight if total_weight else 0.0
        score = round(max(0.0, min(1.0, combined_score)), 4)

        if not reasons:
            reasons.append("No strong anomaly signal detected in this sentence")

        return SentenceDecision(sentence=sentence, score=score, reasons=reasons[:3])

    def to_highlight(self, sentence_decision: SentenceDecision, features: SentenceFeature) -> SentenceHighlight:
        status = self._determine_status(sentence_decision.score)
        confidence = max(0.0, min(1.0, sentence_decision.score))
        extracted_features = {
            "perplexity": round(features.readability_score, 4),
            "burstiness": round(features.burstiness, 4),
            "vocabulary_diversity": round(features.vocabulary_diversity, 4),
            "readability_score": round(features.readability_score, 4),
            "entropy": round(features.entropy, 4),
            "repeated_phrase_ratio": round(features.repeated_phrase_ratio, 4),
            "transition_word_frequency": round(features.transition_word_frequency, 4),
            "sentence_complexity": round(features.sentence_complexity, 4),
            "lexical_richness": round(features.lexical_richness, 4),
        }
        return SentenceHighlight(
            sentence=sentence_decision.sentence,
            score=sentence_decision.score,
            confidence=confidence,
            reasons=sentence_decision.reasons,
            extracted_features=extracted_features,
            status=status,
        )

    def score_essay(self, sentences: list[str], sentence_features: list[SentenceFeature]) -> EssayDecision:
        sentence_decisions = [
            self.score_sentence(sentence, features)
            for sentence, features in zip(sentences, sentence_features)
        ]
        overall_score = sum(item.score for item in sentence_decisions) / len(sentence_decisions) if sentence_decisions else 0.0
        return EssayDecision(overall_score=round(overall_score, 4), sentence_scores=sentence_decisions)

    def score_with_highlights(self, sentences: list[str], sentence_features: list[SentenceFeature]) -> DetectionResult:
        decisions = [
            self.score_sentence(sentence, features)
            for sentence, features in zip(sentences, sentence_features)
        ]
        overall_score = sum(item.score for item in decisions) / len(decisions) if decisions else 0.0
        highlights = [
            self.to_highlight(decision, features)
            for decision, features in zip(decisions, sentence_features)
        ]
        return DetectionResult(overall_score=round(overall_score, 4), sentence_highlights=highlights)
