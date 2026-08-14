from __future__ import annotations

from dataclasses import dataclass, field

from app.models.detection import DetectionResult, SentenceHighlight
from app.models.features import SentenceFeature
from app.utils.perplexity import LocalPerplexityCalculator


@dataclass
class SentenceDecision:
    sentence: str
    score: float
    perplexity: float = 0.0
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
        if score >= 0.6:
            return "likely_ai"
        if score >= 0.35:
            return "suspicious"
        return "likely_human"

    def _risk_for_perplexity(self, perplexity: float) -> float:
        if perplexity <= 70.0:
            return 0.0
        if perplexity >= 160.0:
            return 1.0
        return (perplexity - 70.0) / 90.0

    def _risk_for_burstiness(self, burstiness: float) -> float:
        if burstiness <= 0.4:
            return 0.0
        if burstiness >= 1.1:
            return 1.0
        return (burstiness - 0.4) / 0.7

    def _risk_for_vocabulary(self, value: float) -> float:
        if 0.45 <= value <= 0.8:
            return 0.0
        if value < 0.45:
            return min(1.0, (0.45 - value) / 0.2)
        return min(1.0, (value - 0.8) / 0.25)

    def _risk_for_readability(self, value: float) -> float:
        if 45.0 <= value <= 70.0:
            return 0.0
        if value < 45.0:
            return min(1.0, (45.0 - value) / 22.0)
        return min(1.0, (value - 70.0) / 30.0)

    def _risk_for_entropy(self, entropy: float) -> float:
        if entropy <= 2.8:
            return 0.0
        if entropy >= 3.8:
            return 1.0
        return (entropy - 2.8) / 1.0

    def _risk_for_repeated_phrase(self, value: float) -> float:
        if value <= 0.02:
            return 0.0
        if value >= 0.12:
            return 1.0
        return (value - 0.02) / 0.10

    def _risk_for_transition_words(self, value: float) -> float:
        if value <= 0.01:
            return 0.0
        if value >= 0.08:
            return 1.0
        return (value - 0.01) / 0.07

    def _risk_for_complexity(self, value: float) -> float:
        if value <= 1.1:
            return 0.0
        if value >= 1.5:
            return 1.0
        return (value - 1.1) / 0.4

    def _risk_for_lexical_richness(self, value: float) -> float:
        if value <= 1.05:
            return 0.0
        if value >= 1.30:
            return 1.0
        return (value - 1.05) / 0.25

    def _risk_for_passive_voice(self, count: int) -> float:
        if count <= 0:
            return 0.0
        if count >= 2:
            return 1.0
        return 0.7

    def score_sentence(self, sentence: str, features: SentenceFeature) -> SentenceDecision:
        perplexity_result = self.perplexity_calculator.score_sentence(sentence)
        perplexity = perplexity_result.perplexity

        reasons: list[str] = []
        weighted_signals: list[tuple[float, float]] = []

        perplexity_risk = self._risk_for_perplexity(perplexity)
        weighted_signals.append((perplexity_risk, 0.04))
        if perplexity_risk > 0.6:
            reasons.append("Perplexity is unusually high for this text style")

        burstiness_risk = self._risk_for_burstiness(features.burstiness)
        weighted_signals.append((burstiness_risk, 0.04))
        if burstiness_risk > 0.6:
            reasons.append("Burstiness pattern is unusually irregular")

        vocab_risk = self._risk_for_vocabulary(features.vocabulary_diversity)
        weighted_signals.append((vocab_risk, 0.04))
        if vocab_risk > 0.6:
            reasons.append("Vocabulary range is unusually extreme for a typical essay")

        readability_risk = self._risk_for_readability(features.readability_score)
        weighted_signals.append((readability_risk, 0.32))
        if readability_risk > 0.6:
            reasons.append("Readability deviates sharply from a typical academic range")

        entropy_risk = self._risk_for_entropy(features.entropy)
        weighted_signals.append((entropy_risk, 0.06))
        if entropy_risk > 0.6:
            reasons.append("Token unpredictability is elevated")

        repeated_phrase_risk = self._risk_for_repeated_phrase(features.repeated_phrase_ratio)
        weighted_signals.append((repeated_phrase_risk, 0.12))
        if repeated_phrase_risk > 0.6:
            reasons.append("Repeated phrase pattern is elevated")

        transition_risk = self._risk_for_transition_words(features.transition_word_frequency)
        weighted_signals.append((transition_risk, 0.16))
        if transition_risk > 0.6:
            reasons.append("Transition wording is unusually frequent")

        complexity_risk = self._risk_for_complexity(features.sentence_complexity)
        weighted_signals.append((complexity_risk, 0.08))
        if complexity_risk > 0.6:
            reasons.append("Sentence rhythm is unusually patterned")

        lexical_risk = self._risk_for_lexical_richness(features.lexical_richness)
        weighted_signals.append((lexical_risk, 0.10))
        if lexical_risk > 0.6:
            reasons.append("Lexical profile is unusually formulaic or compressed")

        passive_risk = self._risk_for_passive_voice(features.passive_voice_count)
        weighted_signals.append((passive_risk, 0.12))
        if passive_risk > 0.6:
            reasons.append("Passive voice is unusually frequent for this sentence")

        total_weight = sum(weight for _, weight in weighted_signals)
        combined_score = sum(signal * weight for signal, weight in weighted_signals) / total_weight if total_weight else 0.0
        score = round(max(0.0, min(1.0, combined_score)), 4)

        if not reasons:
            reasons.append("No strong anomaly signal detected in this sentence")

        return SentenceDecision(sentence=sentence, score=score, perplexity=perplexity, reasons=reasons[:3])

    def to_highlight(self, sentence_decision: SentenceDecision, features: SentenceFeature) -> SentenceHighlight:
        status = self._determine_status(sentence_decision.score)
        confidence = max(0.0, min(1.0, sentence_decision.score))
        extracted_features = {
            "perplexity": round(sentence_decision.perplexity, 4),
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
