from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SentenceHighlight:
    sentence: str
    score: float
    confidence: float
    reasons: list[str] = field(default_factory=list)
    extracted_features: dict[str, float | int | str] = field(default_factory=dict)
    status: str = "suspicious"


@dataclass
class DetectionResult:
    overall_score: float
    sentence_highlights: list[SentenceHighlight] = field(default_factory=list)
