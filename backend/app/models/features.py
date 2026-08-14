from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SentenceFeature:
    """Feature set derived from a single sentence."""

    sentence_index: int
    sentence_text: str
    sentence_length: int
    average_word_length: float
    vocabulary_diversity: float
    lexical_richness: float
    repeated_word_ratio: float
    repeated_phrase_ratio: float
    transition_word_frequency: float
    passive_voice_count: int
    readability_score: float
    sentence_complexity: float
    punctuation_frequency: float
    capitalization_patterns: dict[str, float] = field(default_factory=dict)
    burstiness: float = 0.0
    entropy: float = 0.0


@dataclass
class EssayFeatures:
    """Aggregate text features extracted from an essay."""

    average_sentence_length: float
    average_word_length: float
    vocabulary_diversity: float
    lexical_richness: float
    repeated_word_ratio: float
    repeated_phrase_ratio: float
    transition_word_frequency: float
    passive_voice_count: int
    readability_score: float
    sentence_complexity: float
    punctuation_frequency: float
    capitalization_patterns: dict[str, float] = field(default_factory=dict)
    burstiness: float = 0.0
    entropy: float = 0.0
    sentence_count: int = 0
    sentence_features: list[SentenceFeature] = field(default_factory=list)
